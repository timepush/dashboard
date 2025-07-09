import { createRouter, createWebHistory } from "vue-router";
import home from "./views/home/home.vue";
import signup from "./views/signup/signup.vue";
import login from "./views/login/login.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: home
  },
  {
    path: "/signup",
    name: "signup",
    component: signup
  },
  {
    path: "/login",
    name: "login",
    component: login
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
