<template>
  <v-layout row wrap>
    <v-flex xs12 v-for="task in tasks" :key="task.todo.id">
      <v-card class="ma-1 pa-1">
        <v-card-title>
          {{ task.todo.title }}
        </v-card-title>
        <v-card-text>
          <v-form lazy-validation>
            <v-text-field
              :value="task.todo.goal"
              lazy
              @change="value => updateGoal(task, value)"
              label="Goal"
              required>
            </v-text-field>
            <v-text-field
              :value="task.todo.estimation"
              number
              lazy
              @change="value => updateEstimation(task, value)"
              label="見積"
              required>
            </v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat @click="finishTask(task)">Finish</v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {

    };
  },
  props: ['tasks'],
  methods: {
    updateGoal(task, newGoal) {
      this.$emit('update-goal', task.todo.id, newGoal);
    },
    updateEstimation(task, newEstimation) {
      this.$emit('update-estimation', task.todo.id, newEstimation);
    },
    finishTask(task) {
      this.$emit('finish-task', task.todo.id);
    }
  },
};
</script>
