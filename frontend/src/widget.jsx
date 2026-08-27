import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import cssText from "./App.css?raw";

const style = document.createElement("style");
style.textContent = cssText;
document.head.appendChild(style);

const container = document.createElement("div");

container.id = "hotel-chatbot-root";

document.body.appendChild(container);

createRoot(container).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);