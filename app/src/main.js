import { createApp } from "vue";
import "./assets/style.css";
import App from "./App.vue";

const app = createApp(App);

// ROUTER
import router from "./router";
app.use(router);

app.mount("#app");
