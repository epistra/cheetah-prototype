import moment from 'moment';

/* eslint class-methods-use-this:
   ["error", { "exceptMethods": ["type", "start", "end", "title"] }] */
class Schedule {
  constructor(id, start, end, title) {
    this.id = id;
    this.start = start;
    this.end = end;
    this.title = title;
  }

  get type() { return 'schedule'; }
  get duration() { return this.end.unix() - this.start.unix(); }
}

class Todo {
  constructor(id, title, goal = '', estimation = 0, isFinished = false) {
    this.id = id;
    this.title = title;
    this.goal = goal;
    this.estimation = estimation;
    this.isFinished = isFinished;
  }

  get type() { return 'todo'; }
  get isValid() { return this.goal !== '' && this.estimation > 0 && !this.isFinished; }
  get duration() { return moment.duration(this.estimation, 'minutes').asSeconds(); }
  update(args) {
    this.title = args.title;
    this.goal = args.goal;
    this.estimation = args.estimation;
    this.isFinished = args.isFinished;
  }
}

class Task {
  constructor(id, todo, start = null) {
    this.id = id;
    this.todo = todo;
    this.start = start;
  }

  get title() { return this.todo.title; }
  get duration() { return this.todo.duration; }
  get isScheduled() { return this.todo.isValid && this.start !== null; }
  get type() { return 'task'; }
  get end() {
    if (this.isScheduled) {
      return moment.unix(this.start.unix() + this.duration);
    }
    return null;
  }
}

class SpareTime {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }

  get type() { return 'spare'; }
  get title() { return '空き'; }
  get duration() { return this.end.unix() - this.start.unix(); }
}

class Tag {
  constructor(id, title, todos) {
    this.id = id;
    this.title = title;
    this.todos = todos;
  }
}

export default {

  getSortedTaskes(tasks) {
    return tasks.slice().sort((l, r) => l.start.unix() - r.start.unix());
  },

  makeTodo(args) { return new Todo(args.id, args.title, args.goal, args.estimation, args.isFinished); },

  makeSchedule(args) { return new Schedule(args.id, args.start, args.end, args.title); },

  makeTask(id, todo) { return new Task(id, todo); },

  makeSpareTime(start, end) { return new SpareTime(start, end); },

  makeTag(args) { return new Tag(args.id, args.title, args.todos); },
};
