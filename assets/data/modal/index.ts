import type { Component, Magic } from "../types";

interface Modal extends Component, Magic {
  status: "open" | "closed";
  removeTimer: number | undefined;
  open: () => void;
  close: () => void;
}

export default function modal(): Modal {
  return {
    status: "closed",
    removeTimer: undefined,
    open() {
      this.status = "open";
    },
    close() {
      this.status = "closed";
      let modalContainer = document.getElementById("modal-container") as HTMLDivElement;
      this.removeTimer = setTimeout(() => {
        modalContainer.innerHTML = "";
      }, 200);
    },
    destroy() {
      clearTimeout(this.removeTimer);
    },
  };
}
