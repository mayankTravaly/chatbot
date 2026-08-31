import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import cssText from "./App.css?raw";

const container = document.createElement("div");

container.id = "hotel-chatbot-root";

document.body.appendChild(container);

const shadowRoot = container.attachShadow({
  mode: "open",
});

const style = document.createElement("style");
style.textContent = cssText;
shadowRoot.appendChild(style);

const appRoot = document.createElement("div");
shadowRoot.appendChild(appRoot);

createRoot(appRoot).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);