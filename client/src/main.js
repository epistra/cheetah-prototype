// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import Vuetify from 'vuetify';
import moment from 'vue-moment';
import DaySpanVuetify from 'dayspan-vuetify';
import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons/iconfont/material-icons.css';
import 'dayspan-vuetify/dist/lib/dayspan-vuetify.min.css';
import App from './App';
import router from './router';

Vue.config.productionTip = false;
Vue.use(Vuetify);
Vue.use(moment);
Vue.use(DaySpanVuetify, {});


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
