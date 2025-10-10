import type { DateInput, Direction } from "./models";
import { dateToString, stringToDate } from "./services";

export default function date(): DateInput {
  return {
    setInput(input: HTMLInputElement, date?: Date) {
      date = date || new Date();
      input.value = dateToString(date);
    },
    handleFocus(el: HTMLInputElement) {
      let date = new Date(el.value);
      if (isNaN(date.getTime()) || !el.value) {
        this.setInput(el);
        el.select();
      }
    },
    changeDay(el: HTMLInputElement, direction: Direction) {
      let date = stringToDate(el.value);
      direction === "up" ? date.setDate(date.getDate() + 1) : date.setDate(date.getDate() - 1);
      this.setInput(el, date);
    },
    changeYear(el: HTMLInputElement, direction: Direction) {
      let date = stringToDate(el.value);
      if (direction === "up") {
        date.setFullYear(date.getFullYear() + 1);
        date.setDate(date.getDate() - 1);
      } else {
        date.setFullYear(date.getFullYear() - 1);
        date.setDate(date.getDate() + 1);
      }
      this.setInput(el, date);
    },
    changeMonth(el: HTMLInputElement, direction: Direction) {
      let date = stringToDate(el.value);
      if (direction === "up") {
        date.setMonth(date.getMonth() + 1);
        date.setDate(date.getDate() - 1);
      } else {
        date.setMonth(date.getMonth() - 1);
        date.setDate(date.getDate() + 1);
      }
      this.setInput(el, date);
    },
  };
}
