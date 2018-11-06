import moment from 'moment';

export default {
  getTime(hour, minute) {
    return moment().locale('ja').set({ hour, minute, second: 0, millisecond: 0 });
  },

  getSortedTaskes(tasks) {
    return tasks.slice().sort((l, r) => l.start.unix() - r.start.unix());
  },

  getRange(start, end) {
    return { start, end };
  },

  getUnixtimeDuration(start, end) {
    return end.unix() - start.unix();
  },

  mergeTimeRanges(ranges) {
    const length = ranges.length;
    const sortedRanges = ranges.slice().sort((l, r) => l.start.unix() - r.start.unix());
    const mergedRanges = [];
    for (let i = 0; i < length; i += 1) {
      const mergedRange = Object.assign(sortedRanges[i], {});
      for (let j = i + 1; j < length; j += 1) {
        const nextRange = sortedRanges[j];
        if (mergedRange.end.unix() < nextRange.start.unix()) { break; }
        if (mergedRange.end.unix() < nextRange.end.unix()) { mergedRange.end = nextRange.end; }
      }
      mergedRanges.push(mergedRange);
    }
    return mergedRanges;
  },

  divideRange(target, divider) {
    if (target.end.unix() <= divider.start.unix() ||
        divider.end.unix() <= target.start.unix()) {
      return [target];
    }

    const dividedRanges = [];
    if (target.start.unix() < divider.start.unix()) {
      dividedRanges.push({ start: target.start, end: divider.start });
    }
    if (divider.end.unix() < target.end.unix()) {
      dividedRanges.push({ start: divider.end, end: target.end });
    }
    return dividedRanges;
  },

  divideRanges(targets, divider) {
    return targets.flatMap(target => this.divideRange(target, divider));
  },

};
