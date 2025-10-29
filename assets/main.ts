import mask from "@alpinejs/mask";
import persist from "@alpinejs/persist";
import Alpine, { type Alpine as AlpineType } from "alpinejs";
import htmx from "htmx.org";
import * as data from "./data";
import "./style.css";

declare global {
  interface Window {
    Alpine: AlpineType;
    htmx: typeof htmx;
  }
}

Alpine.plugin(persist);
Alpine.plugin(mask);

Alpine.data("colorTheme", data.colorTheme);
Alpine.data("body", data.body);
Alpine.data("date", data.inputs.date);
Alpine.data("modal", data.modal);

Alpine.start();
