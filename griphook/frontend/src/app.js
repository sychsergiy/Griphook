import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";

import PeaksPage from "./peaks/index";
import AdminPage from "./admin/index";
import BillingPage from "./billing/index";

import HeaderComponent from "./common/headerComponent";

class App extends Component {
  render() {
    return (
      <div>
        <HeaderComponent />
        <Switch>
          <Route exact path="/" component={BillingPage} />
          <Route path="/peaks" component={PeaksPage} />
          <Route path="/billing" component={BillingPage} />
          <Route path="/admin" component={AdminPage} />
        </Switch>
      </div>
    );
  }
}

export default App;
