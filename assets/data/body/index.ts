import type { Component, Magic } from "../types";

interface Body extends Component, Magic {
  pageTitle: string;
}

export default function body(pageTitle: string): Body {
  return {
    pageTitle,
    init() {
      document.title = this.pageTitle;
    },
  };
}
