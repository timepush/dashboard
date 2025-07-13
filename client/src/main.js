import { createApp } from "vue";
import "./assets/style.css";
import App from "./App.vue";

const app = createApp(App);

// TOOLTIP
import Tooltip from "vue-follow-tooltip";
app.use(Tooltip, {
  delay: 100,
  center: false,
  offsetX: 0,
  offsetY: 20
});

// ROUTER
import router from "./router";
app.use(router);

app.mount("#app");
