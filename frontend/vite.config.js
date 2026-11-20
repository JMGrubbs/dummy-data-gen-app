import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["ddata-dummy.johnmgrubbs.io", "data-dummy.johnmgrubbs.io"],
  },
});
