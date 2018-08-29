import React, { Component } from "react";
import { connect } from "react-redux";
import { Switch, Route } from "react-router-dom";

import SettingsMenuComponent from "./common/settingsMenuComponent";

import TasksSettingsPage from "./tasks";
import ResourcesSettingsPage from "./resources";


class SettingsPage extends Component {
  render() {
    return (
      <div className="container">
        <div className="d-flex flex-wrap flex-md-nowrap">
          <SettingsMenuComponent />

          <Switch>
            <Route exact path="/settings" component={TasksSettingsPage} />
            <Route path="/settings/tasks" component={TasksSettingsPage} />
            <Route path="/settings/resources" component={ResourcesSettingsPage} />
          </Switch>
        </div>
      </div>
    );
  }
}

export default SettingsPage;
