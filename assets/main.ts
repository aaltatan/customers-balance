import focus from "@alpinejs/focus";
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

// htmx configurations
document.addEventListener("htmx:load", () => {
  htmx.config.defaultSwapStyle = "outerHTML";
  htmx.config.globalViewTransitions = true;
  htmx.config.refreshOnHistoryMiss = true;
  htmx.config.historyCacheSize = 0;
  htmx.config.historyRestoreAsHxRequest = false;
});

Alpine.plugin(focus);
Alpine.plugin(mask);
Alpine.plugin(persist);

Alpine.data("colorTheme", data.colorTheme);
Alpine.data("body", data.body);
Alpine.data("date", data.inputs.date);
Alpine.data("modal", data.modal);

Alpine.start();
