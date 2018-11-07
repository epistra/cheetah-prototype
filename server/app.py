import datetime
import json
import os
import time
import click
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "cheetah-dev.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
Migrate(app, db)


# Models
tags_todos = db.Table(
    'tags_todos',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('todo_id', db.Integer, db.ForeignKey('todos.id'), primary_key=True)
)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    goal = db.Column(db.String(255), nullable=False, default="")
    estimation = db.Column(db.Integer, nullable=False, default=0)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "goal": self.goal,
            "estimation": self.estimation
        }


class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start": time.mktime(self.start.timetuple()),
            "end": time.mktime(self.end.timetuple())
        }


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey("todos.id"))
    start = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        return {
            "id": self.id,
            "todo_id": self.todo_id,
            "start": self.start
        }


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    todos = db.relationship('Todo', secondary=tags_todos, lazy="subquery",
                            backref=db.backref("todos", lazy=True))

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "todos": [todo.as_dict() for todo in self.todos]
        }


# APIs
# Todos
@app.route("/api/v1/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return (jsonify([todo.as_dict() for todo in todos]), 200)


@app.route("/api/v1/todos", methods=["POST"])
def add_todo():
    content = json.loads(request.data)
    todo = Todo(title=content["title"])
    db.session.add(todo)
    db.session.commit()
    return (jsonify(todo.as_dict()), 201)


@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    content = json.loads(request.data)
    todo = Todo.query.filter(Todo.id == todo_id).first()
    todo.title = content["title"]
    todo.goal = content["goal"]
    todo.estimation = content["estimation"]
    db.session.commit()
    return (jsonify(todo.as_dict()), 201)


# Schedules
@app.route("/api/v1/schedules", methods=["GET"])
def get_schedules():
    schedules = Schedule.query.all()
    return (jsonify([schedule.as_dict() for schedule in schedules]), 200)


@app.route("/api/v1/schedules", methods=["POST"])
def add_schedule():
    content = json.loads(request.data)
    start = datetime.datetime.fromtimestamp(content["start"])
    end = datetime.datetime.fromtimestamp(content["end"])
    schedule = Schedule(title=content["title"], start=start, end=end)
    db.session.add(schedule)
    db.session.commit()
    return (jsonify(schedule.as_dict()), 201)


# Tasks
@app.route("/api/v1/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return (jsonify([task.as_dict() for task in tasks]), 200)


@app.route("/api/v1/tasks", methods=["POST"])
def create_task():
    content = json.loads(request.data)
    task = Task(todo_id=content["todo_id"])
    db.session.add(task)
    db.session.commit()
    return (jsonify(task.as_dict()), 201)


@app.route("/api/v1/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    Task.query.filter(Task.id == task_id).delete()
    db.session.commit()
    return ("", 204)


# Tags
@app.route("/api/v1/tags", methods=["GET"])
def get_tags():
    tags = Tag.query.all()
    return (jsonify([tag.as_dict() for tag in tags]), 200)


@app.route("/api/v1/tags/<int:tag_id>/todos", methods=["POST"])
def add_tag_item(tag_id):
    content = json.loads(request.data)
    tag = Tag.query.filter(Tag.id == tag_id).first()
    todo = Todo.query.filter(Todo.id == content["todo_id"]).first()
    tag.todos.append(todo)
    db.session.add(tag)
    db.session.commit()
    return (jsonify(tag.as_dict()), 201)


# db initialization
@app.cli.command()
def init_db():
    confirmation = input("Drop, Create and Initialize all tables? [y/N] ").lower()
    if confirmation not in ["y", "yes"]:
        return
    db.drop_all()
    db.create_all()

    todos = [Todo(title="Todo {}".format(i+1)) for i in range(8)]
    for todo in todos:
        db.session.add(todo)

    tags = [
        Tag(title="Tag 1", todos=todos[0:3]),
        Tag(title="Tag 2", todos=todos[3:5]),
        Tag(title="Tag 3", todos=todos[5:])
    ]
    for tag in tags:
        db.session.add(tag)

    def get_time(hour):
        return datetime.datetime.today().replace(hour=hour, minute=0, second=0, microsecond=0)

    schedules = [
        Schedule(title="Schedule 1", start=get_time(12), end=get_time(13)),
        Schedule(title="Schedule 2", start=get_time(14), end=get_time(15)),
    ]
    for schedule in schedules:
        db.session.add(schedule)

    db.session.commit()
    print("Finished initializing all tables.")


if __name__ == "__main__":
    app.run()
