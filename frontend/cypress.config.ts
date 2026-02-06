import { defineConfig } from "cypress";
import vitePreprocessor from "cypress-vite";

export default defineConfig({
  e2e: {
    baseUrl: "http://localhost:3000",
    specPattern: "tests/**/*.cy.{js,jsx,ts,tsx}",
    supportFile: false,
    setupNodeEvents(on) {
      on("file:preprocessor", vitePreprocessor());
    },
  },
});
