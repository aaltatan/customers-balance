import { Color, type ColorTheme, type Theme } from "./models";

export default function colorTheme(): ColorTheme {
  return {
    theme: "system",
    get isSystemDark() {
      return matchMedia("(prefers-color-scheme: dark)").matches;
    },
    get isDark(): boolean {
      return this.theme === "dark" || (this.theme === "system" && this.isSystemDark);
    },
    get backgroundColor(): Color {
      switch (this.theme) {
        case "light":
          return Color.Light;
        case "dark":
          return Color.Dark;
        case "system":
          return this.isSystemDark ? Color.Dark : Color.Light;
      }
    },
    init() {
      this.theme = (localStorage.getItem("color-theme") as Theme) || this.theme;
      this.setTheme(this.theme);
    },
    setTheme(value: Theme) {
      this.theme = value;
      if (value === "system") {
        localStorage.removeItem("color-theme");
      } else {
        localStorage.setItem("color-theme", value);
      }
    },
    toggleTheme() {
      if (this.theme === "light") {
        this.setTheme("dark");
        return;
      } else if (this.theme === "dark") {
        this.setTheme("system");
        return;
      } else {
        this.setTheme("light");
      }
    },
  };
}
