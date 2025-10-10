import type { Component, Magic } from "../../types";

export interface DateInput extends Component, Magic {
  setInput: (target: HTMLInputElement, date?: Date) => void;
  handleFocus: (el: HTMLInputElement) => void;
  changeDay: (el: HTMLInputElement, direction: Direction) => void;
  changeYear: (el: HTMLInputElement, direction: Direction) => void;
  changeMonth: (el: HTMLInputElement, direction: Direction) => void;
}

export type Direction = "up" | "down";