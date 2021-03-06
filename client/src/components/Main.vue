<template>
  <v-app>
    <navigation-bar></navigation-bar>
    <v-container fluid text-xs-center>
      <v-layout row wrap>
        <v-flex xs4 class="pa-1">
          <todolist
            :tags="tags"
            :tasks="tasks"
            @add-todo="addTodo"
            @toggle-execution="toggleExecution"/>
        </v-flex>
        <v-flex xs4 class="pa-1">
          <tasklist
            :tasks="tasks"
            @update-goal="updateTodoGoal"
            @update-estimation="updateTodoEstimation"
            @finish-task="finishTask"/>
        </v-flex>
        <v-flex xs4 class="pa-1">
          <timeline
            :tasks="scheduledTasks"
            :schedules="todaysSchedules"
            @add-schedule="addSchedule"/>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import moment from 'moment';
import axiosbase from 'axios';
import NavigationVar from './NavigationBar';
import Calendar from './Calendar';
import TodoList from './TodoList';
import TaskList from './TaskList';
import Timeline from './Timeline';
import items from './items';
import momentUtils from './momentUtils';

const axios = axiosbase.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
  responseType: 'json',
});

export default {
  data() {
    const todos = [];
    const tags = [];
    const schedules = [];
    const tasks = [];
    const workingHours = momentUtils.getRange(
      momentUtils.getTime(9, 0), momentUtils.getTime(23, 0));
    return {
      todos,
      tags,
      schedules,
      tasks,
      workingHours,
    };
  },
  created() {
    try {
      this.loadItems();
    } catch (e) {
      console.error(e);
    }
  },
  components: {
    'navigation-bar': NavigationVar,
    todolist: TodoList,
    tasklist: TaskList,
    calendar: Calendar,
    timeline: Timeline,
  },
  computed: {
    scheduledTasks() {
      return this.tasks.filter(task => task.isScheduled);
    },
    todaysSchedules() {
      const today = momentUtils.getTodayRange();
      return this.schedules.filter(s => momentUtils.contain(today, s));
    },
  },
  methods: {
    async loadItems() {
      const todoResponse = await axios.get('/api/v1/todos');
      todoResponse.data.forEach(datum => this.todos.push(items.makeTodo(datum)));
      const tagResponse = await axios.get('/api/v1/tags');
      tagResponse.data.forEach((datum) => {
        const todos = datum.todos.map(todo => this.getTodo(todo.id));
        const args = Object.assign({}, datum, { todos });
        this.tags.push(items.makeTag(args));
      });
      const taskResponse = await axios.get('/api/v1/tasks');
      taskResponse.data.forEach((datum) => {
        const todo = this.getTodo(datum.todo_id);
        this.tasks.push(items.makeTask(datum.id, todo));
      });
      const scheduleResponse = await axios.get('/api/v1/schedules');
      scheduleResponse.data.forEach((datum) => {
        const args = Object.assign({}, datum, {
          start: moment.unix(datum.start).local(),
          end: moment.unix(datum.end).local(),
        });
        this.schedules.push(items.makeSchedule(args));
      });
      this.allocateTasks();
    },

    async updateTodo(todoId, _args) {
      const todo = this.getTodo(todoId);
      const args = Object.assign({}, todo, _args);
      const response = await axios.put(`/api/v1/todos/${todoId}`, args);
      todo.update(response.data);
      return todo;
    },

    getTodo(todoId) {
      return this.todos.find(t => t.id === todoId);
    },

    getTask(todoId) {
      return this.tasks.find(t => t.todo.id === todoId);
    },

    getTag(tagId) {
      return this.tags.find(t => t.id === tagId);
    },

    async toggleExecution(todoId) {
      const todo = this.getTodo(todoId);
      const taskIndex = this.tasks.findIndex(t => t.todo.id === todoId);
      if (taskIndex === -1) {
        const response = await axios.post('/api/v1/tasks', { todo_id: todo.id });
        const task = items.makeTask(response.data.id, todo);
        this.tasks.push(task);
      } else {
        const task = this.tasks[taskIndex];
        await axios.delete(`/api/v1/tasks/${task.id}`);
        this.tasks.splice(taskIndex, 1);
      }
      this.allocateTasks();
    },

    updateTodoGoal(todoId, newGoal) {
      this.updateTodo(todoId, { goal: newGoal });
    },

    async updateTodoEstimation(todoId, newEstimation) {
      await this.updateTodo(todoId, { estimation: parseInt(newEstimation, 10) });
      const task = this.getTask(todoId);
      if (task) {
        this.allocateTasks();
      }
    },

    async addTodo(title, tagId) {
      const todoResponse = await axios.post('/api/v1/todos', { title });
      const todo = items.makeTodo(todoResponse.data);
      this.todos.push(todo);
      const tagResponse = await axios.post(`/api/v1/tags/${tagId}/todos`, { todo_id: todo.id });
      const tag = this.getTag(tagResponse.data.id);
      tag.todos.push(todo); // TODO: update tag using a post request response
      return todo;
    },

    async finishTask(todoId) {
      await this.toggleExecution(todoId); // TODO: Save task history
      const todo = await this.updateTodo(todoId, { isFinished: true });
      return todo;
    },

    async addSchedule(title, start, end) {
      const response = await axios.post('/api/v1/schedules', { title, start, end });
      const args = Object.assign({}, response.data, {
        start: moment.unix(response.data.start).local(),
        end: moment.unix(response.data.end).local(),
      });
      const schedule = items.makeSchedule(args);
      this.schedules.push(schedule);
      return schedule;
    },

    allocateTasks() {
      this.tasks.forEach(task => this.allocateTask(task));
    },

    allocateTask(task) {
      task.start = null;
      if (!task.todo.isValid) { return; }
      const spareTimes = this.getSpareTimes();
      const i = spareTimes.findIndex(spare => spare.duration >= task.duration);
      if (i < 0) { return; }

      const spareTime = spareTimes[i];
      task.start = spareTime.start;
    },

    getSpareTimes() {
      const baseRange = [this.workingHours];
      const tasks = this.schedules
        .slice()
        .concat(this.tasks.filter(task => task.isScheduled))
        .map(item => momentUtils.getRange(item.start, item.end));
      const mergedTaskRanges = momentUtils.mergeTimeRanges(tasks);
      return mergedTaskRanges
        .reduce((acc, d) => momentUtils.divideRanges(acc, d), baseRange)
        .map(range => items.makeSpareTime(range.start, range.end));
    },
  },
};
</script>
