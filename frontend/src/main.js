import Vue from 'vue';
import router from './router';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import HelloWorld from '@/components/HelloWorld';

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;

new Vue({
  router,
  render: h => h(HelloWorld),
}).$mount('#app');