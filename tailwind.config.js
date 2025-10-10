/** @type {import('tailwindcss').Config} */

const plugin = require("tailwindcss/plugin");

export default {
  darkMode: "selector",
  content: ["templates/**/*.html", "apps/**/*.html", "assets/**/*.ts"],
  theme: {
    extend: {},
  },
  plugins: [
    plugin(function ({ addVariant }) {
      addVariant("has-checked", "&:has(input:checked)");
      addVariant("hx-request", "&.htmx-request");
      addVariant("hx-swap", "&.htmx-swapping");
      addVariant("hx-settle", "&.htmx-settling");
      addVariant("active", "&.active");
      addVariant("dark", "&:where(.dark, .dark *)");
      addVariant("tb-td", "& table td");
      addVariant("tb-th", "& table th");
    }),
  ],
};
