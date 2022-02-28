import Vue from 'vue';
import axios from 'axios';
import HelloWorld from '@/components/HelloWorld';

Vue.config.productionTip = false;
Vue.prototype.$axios = axios;

new Vue({
  render: h => h(HelloWorld),
}).$mount('#app');