import { createRouter, createWebHistory } from "vue-router";
import home from "@/views/home/home.vue";
import signup from "@/views/auth/signup.vue";
import signin from "@/views/auth/signin.vue";
import dashboard from "@/views/dashboard/dashboard.vue";
import { getAccessToken, refreshToken } from "@/lib/auth";

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
    path: "/signin",
    name: "signin",
    component: signin
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: dashboard,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

let refreshing = null;
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth && !getAccessToken()) {
    // Only try to refresh once per navigation
    if (!refreshing) {
      refreshing = refreshToken().catch(() => null);
    }
    const token = await refreshing;
    refreshing = null;
    if (getAccessToken()) {
      next();
    } else {
      next({ name: "signin" });
    }
  } else {
    next();
  }
});

export default router;
