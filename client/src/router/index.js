import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '../components/Login.vue';
import Messages from '../components/Messages.vue';

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login,
    },
    {
      path: '/messages',
      name: 'Messages',
      component: Messages,
    },
  ],
});

export default router;
