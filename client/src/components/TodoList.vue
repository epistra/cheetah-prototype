<template>
  <v-tabs>
    <v-tab v-for="tag in tags" :key="tag.id">
      {{ tag.title }}
    </v-tab>
    <v-tab-item v-for="tag in tags" :key="tag.id">
      <v-card>
        <v-list>
          <v-list-tile v-for="todo in tag.todos" :key="todo.id">
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
    </v-tab-item>
  </v-tabs>
</template>

<script>
export default {
  data() {
    return {

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
  },
};
</script>
