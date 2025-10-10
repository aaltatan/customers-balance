import type { Component, Magic } from "../types";

export enum Color {
  Light = "#ffffff",
  Dark = "#000000",
}

export type Theme = "light" | "dark" | "system";

export interface ColorTheme extends Component, Magic {
  theme: Theme;
  isSystemDark: boolean;
  isDark: boolean;
  backgroundColor: Color;
  setTheme: (value: Theme) => void;
  toggleTheme: () => void;
}
