import React, { Component } from "react";
import { Switch, Route } from "react-router-dom";

import {TabClustersResourcesComponent} from "./components/tabClustersResources"
import {TabServersResourcesComponent} from "./components/tabServersResources"
import {TabsMenuComponent} from "./components/tabsMenu"


class ResourcesSettingsPage extends Component {
  render() {
    return(
        <div className="content flex-grow-1 flex-shrink-1 mt-4 mx-md-1 mx-lg-4">
            <h3>Resources settings</h3>
            <p className="text-muted">Set cpu and memory price for servers and clusters</p>
            <TabsMenuComponent />

            <div className="tab-content border border-top-0 pt-3 px-2">
                <Switch>
                  <Route path="/settings/resources/servers" component={TabServersResourcesComponent} />
                  <Route path="/settings/resources/clusters" component={TabClustersResourcesComponent} />
                </Switch>
            </div>
        </div>
    );
  }
}

export default ResourcesSettingsPage;