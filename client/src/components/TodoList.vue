<template>
  <v-tabs v-model="activeTab">
    <v-tab v-for="tag in tags" :key="tag.id">
      {{ tag.title }}
    </v-tab>
    <v-tab-item v-for="tag in tags" :key="tag.id">
      <v-card>
        <v-list>
          <v-list-tile
            v-for="todo in tag.todos.filter(t => !t.isFinished)"
            :key="todo.id">
            <v-layout row wrap>
              <v-flex xs11 text-xs-left>{{ todo.title }}</v-flex>
              <v-flex xs1>
                <v-checkbox
                  :value="isTarget(todo)"
                  @click.native="toggleTarget(todo)"/>
              </v-flex>
            </v-layout>
          </v-list-tile>
        </v-list>
      </v-card>
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click.native="openTodoAdditionDialog()">Add Todo</v-btn>
          <v-dialog v-model="dialog.active" max-width="600px">
            <v-card>
              <v-card-title>
                Add Todo
              </v-card-title>
              <v-card-text>
                <v-form lazy-validation>
                  <v-text-field v-model="dialog.title" lazy label="Title"/>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn flat @click="addTodo()">submit</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-actions>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
export default {
  data() {
    return {
      activeTab: null,
      dialog: {
        active: false,
        title: '',
      },
    };
  },
  props: ['tags', 'tasks'],
  methods: {
    isTarget(todo) {
      return this.tasks.findIndex(t => t.todo.id === todo.id) >= 0;
    },
    toggleTarget(todo) {
      this.$emit('toggle-execution', todo.id);
    },
    openTodoAdditionDialog() {
      this.dialog.active = true;
    },
    addTodo() {
      this.$emit('add-todo', this.dialog.title, this.tags[this.activeTab].id);
      this.dialog.active = false;
      this.dialog.title = '';
    },
  },
};
</script>
