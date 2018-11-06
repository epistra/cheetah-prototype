<template>
  <div>
    <v-timeline align-top dense>
      <v-timeline-item
        small
        v-for="item in scheduledItems"
        :color="getTimelineColor(item)"
        :key="item.id">
        <v-layout pt-3>
          <v-flex xs3>
            <strong>{{ item.start | moment("HH:mm") }}</strong>
             - <strong>{{ item.end | moment("HH:mm") }}</strong>
          </v-flex>
          <v-flex>
            <strong>{{ item.title }}</strong>
          </v-flex>
        </v-layout>
      </v-timeline-item>
    </v-timeline>
  </div>
</template>

<script>
import momentUtils from './momentUtils';

export default {
  props: ['tasks', 'schedules'],
  data() {
    return {
      startTime: momentUtils.getTime(9, 0),
      endTime: momentUtils.getTime(23, 0),
    };
  },
  computed: {
    scheduledItems() {
      const items = this.tasks.slice().concat(this.schedules);
      return momentUtils.getSortedTaskes(items);
    },
  },
  methods: {
    getId(item) {
      return `${item.type}-${item.id}`;
    },

    getTimelineColor(item) {
      return {
        task: 'primary',
        schedule: 'secondary',
      }[item.type] || 'error';
    },
  },
};

</script>
