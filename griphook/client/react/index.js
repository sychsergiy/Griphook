import React from "react";
import ReactDom from "react-dom";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

import configureStore from "./redux/createStore";

import App from "./app";

const store = configureStore();

ReactDom.render(
  <Provider store={store}>
      <App />
  </Provider>,
  document.getElementById("app")
);
