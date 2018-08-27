import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";

import PeaksPage from "./peaks/index";
import BillingPage from "./billing/index";
import SettingsPage from "./admin/index";

import HeaderComponent from "./common/headerComponent";

import "./main.css";

class App extends Component {
  render() {
    return (
      <div>
        <HeaderComponent />
        <Switch>
          <Route exact path="/" component={BillingPage} />
          <Route path="/peaks" component={PeaksPage} />
          <Route path="/billing" component={BillingPage} />
          <Route path="/settings" component={SettingsPage} />
        </Switch>
      </div>
    );
  }
}

export default App;
