<template>
  <v-card>
    <v-card-text>
      <v-timeline align-top dense>
        <v-timeline-item
          small
          v-for="item in scheduledItems"
          :color="getTimelineColor(item)"
          :key="getItemKey(item)">
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
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn flat @click.native="dialog.active = true">Add Schedule</v-btn>
      <v-dialog v-model="dialog.active" max-width="600px">
        <v-card>
          <v-card-title>
            Add Schedule
          </v-card-title>
          <v-card-text>
            <v-form lazy-validation>
              <v-text-field v-model="dialog.title" lazy label="Title"/>
              <!-- TODO refactor pickers -->
              <v-layout>
                <v-flex xs6>
                  <v-menu
                    ref="startDatePicker"
                    :close-on-content-click="false"
                    v-model="dialog.startDatePicker"
                    :nudge-right="40"
                    :return-value.sync="dialog.startDate"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    min-width="290px"
                  >
                    <v-text-field
                      slot="activator"
                      v-model="dialog.startDate"
                      label="Start date"
                      prepend-icon="event"
                      readonly
                    ></v-text-field>
                    <v-date-picker v-model="dialog.startDate" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="$refs.startDatePicker.save(dialog.startDate)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs6>
                  <v-menu
                     ref="startTimePicker"
                     :close-on-content-click="false"
                     v-model="dialog.startTimePicker"
                     :nudge-right="40"
                     :return-value.sync="dialog.startTime"
                     lazy
                     transition="scale-transition"
                     offset-y
                     full-width
                     max-width="290px"
                     min-width="290px"
                   >
                     <v-text-field
                       slot="activator"
                       v-model="dialog.startTime"
                       label="Start Time"
                       prepend-icon="access_time"
                       readonly/>
                     <v-time-picker
                       v-if="dialog.startTimePicker"
                       v-model="dialog.startTime"
                       full-width>
                       <v-spacer></v-spacer>
                       <v-btn flat color="primary" @click="$refs.startTimePicker.save(dialog.startTime)">OK</v-btn>
                     </v-time-picker>
                   </v-menu>
                </v-flex>
              </v-layout>
              <v-layout>
                <v-flex xs6>
                  <v-menu
                    ref="endDatePicker"
                    :close-on-content-click="false"
                    v-model="dialog.endDatePicker"
                    :nudge-right="40"
                    :return-value.sync="dialog.endDate"
                    lazy
                    transition="scale-transition"
                    offset-y
                    full-width
                    min-width="290px"
                  >
                    <v-text-field
                      slot="activator"
                      v-model="dialog.endDate"
                      label="End date"
                      prepend-icon="event"
                      readonly
                    ></v-text-field>
                    <v-date-picker v-model="dialog.endDate" no-title scrollable>
                      <v-spacer></v-spacer>
                      <v-btn flat color="primary" @click="$refs.endDatePicker.save(dialog.endDate)">OK</v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-flex>
                <v-flex xs6>
                  <v-menu
                     ref="endTimePicker"
                     :close-on-content-click="false"
                     v-model="dialog.endTimePicker"
                     :nudge-right="40"
                     :return-value.sync="dialog.endTime"
                     lazy
                     transition="scale-transition"
                     offset-y
                     full-width
                     max-width="290px"
                     min-width="290px"
                   >
                     <v-text-field
                       slot="activator"
                       v-model="dialog.endTime"
                       label="End Time"
                       prepend-icon="access_time"
                       readonly/>
                     <v-time-picker
                       v-if="dialog.endTimePicker"
                       v-model="dialog.endTime"
                       full-width>
                       <v-spacer></v-spacer>
                       <v-btn flat color="primary" @click="$refs.endTimePicker.save(dialog.endTime)">OK</v-btn>
                     </v-time-picker>
                   </v-menu>
                </v-flex>
              </v-layout>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn flat @click="addSchedule()">submit</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script>
import moment from 'moment';
import momentUtils from './momentUtils';

export default {
  props: ['tasks', 'schedules'],
  data() {
    return {
      dialog: this.getInitialDialogState(),
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
    getItemKey(item) {
      return `${item.type}-${item.id}`;
    },
    getTimelineColor(item) {
      return {
        task: 'primary',
        schedule: 'secondary',
      }[item.type] || 'error';
    },
    getInitialDialogState() {
      return {
        active: false,
        title: '',
        startDate: moment().local('ja').format('YYYY-MM-DD'), // TODO: refactor this
        startTime: null,
        endDate: moment().local('ja').format('YYYY-MM-DD'),
        endTime: null,
        startDatePicker: false,
        startTimePicker: false,
        endDatePicker: false,
        endTimePicker: false,
      }
    },
    addSchedule() {
      const startTime = moment(`${this.dialog.startDate} ${this.dialog.startTime}`).locale('ja').unix();
      const endTime = moment(`${this.dialog.endDate} ${this.dialog.endTime}`).locale('ja').unix();
      this.$emit('add-schedule', this.dialog.title, startTime, endTime);
      this.dialog = this.getInitialDialogState();
    }
  },
};

</script>
