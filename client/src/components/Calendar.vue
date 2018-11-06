<template>
  <div>
    <ds-day-picker :span="calendar.span"/>
  </div>
</template>

<script>
import { Calendar } from 'dayspan';

export default {
  props: {
    calendar:
    {
      type: Calendar,
      default() {
        return Calendar.months();
      },
    },
    readOnly:
    {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      message: 'hoge',
    };
  },
};
</script>
