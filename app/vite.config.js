import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
import Icons from "unplugin-icons/vite";
import { resolve } from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss(), Icons()],
  envDir: resolve(__dirname, ".."),
  resolve: {
    alias: {
      // make `@` point to `<projectRoot>/src`
      "@": resolve(__dirname, "src")
    }
  }
});
