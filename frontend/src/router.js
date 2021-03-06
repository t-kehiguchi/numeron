import Vue from 'vue';
import Router from 'vue-router';
import Detail from '@/views/detail';
import Index from '@/views/index';
import Ranking from '@/views/ranking';
import Login from '@/views/login';
import New from '@/views/new';

Vue.use(Router);

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/new',
    name: 'new',
    component: New
  },
  {
    path: '/detail/:id',
    name: 'detail',
    component: Detail
  },
  {
    path: '/index',
    name: 'index',
    component: Index
  },
  {
    path: '/ranking',
    name: 'ranking',
    component: Ranking
  },
];

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;