import React from "react";
import ReactDom from "react-dom";
import { Provider } from "react-redux";
import { HashRouter } from "react-router-dom";

import configureStore from "./createStore";

import App from "./app";

const store = configureStore();

ReactDom.render(
  <Provider store={store}>
    <HashRouter>
      <App />
    </HashRouter>
  </Provider>,
  document.getElementById("app")
);
