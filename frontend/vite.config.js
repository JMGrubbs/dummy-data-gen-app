import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: ["vm-work-dev-db.tail0c3733.ts.net", "*"],
  },
});
