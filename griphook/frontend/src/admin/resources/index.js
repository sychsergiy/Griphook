import React, { Component } from "react";
import { NavLink } from "react-router-dom";
import { Switch, Route } from "react-router-dom";

import TableServersBodyContainer from './containers/tableServersBody'
import TableClustersBodyContainer from './containers/tableClustersBody'


export const getErrorInformation = (errorData) => {
    let error = 'Error information: ';
    errorData.forEach((item) => {(error += item.msg + "; ")});
    return error
};


export const TabsMenuComponent = () => {
  return (
        <ul className="nav nav-tabs">
            <li className="nav-item">
                <NavLink to="/settings/resources/servers" className="nav-link" activeClassName="active">
                    <i className="fas fa-server mr-2"></i>
                    Servers
                </NavLink>
            </li>
            <li className="nav-item">
                <NavLink to="/settings/resources/clusters" className="nav-link" activeClassName="active">
                    <i className="fas fa-th-large mr-2"></i>
                    Clusters
                </NavLink>
            </li>
        </ul>
  );
};


export const TableHeaderComponent = () => {
  return (
        <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">CPU Price <i className="fas fa-dollar-sign"></i></th>
              <th scope="col">Memory Price <i className="fas fa-dollar-sign"></i></th>
            </tr>
        </thead>
  );
};


class InputBoxContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
        value: this.props.value,
        toolIsActive: false
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleClickAccept = this.handleClickAccept.bind(this);
    this.handleClickCancel = this.handleClickCancel.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value, toolIsActive: true});
  }

  handleClickAccept() {
    this.setState({toolIsActive: false});
    if (this.state.value === "") {
        this.props.updateObject(this.props.objectId, NaN);
    }
    else {
        this.props.updateObject(this.props.objectId, this.state.value);
    }
  }

  handleClickCancel() {
    this.setState({value: this.props.value, toolIsActive: false});
  }

  render() {
    const inputToolClassName = this.state.toolIsActive ? "input-tools" : "input-tools hidden";
    return (
        <td>
            <div className="position-relative">
                <input className="input-price" value={this.state.value} placeholder="Price" type="text" onChange={this.handleChange} />
                    <div className={inputToolClassName}>
                        <i className="fas fa-check accept" onClick={this.handleClickAccept}></i>
                        <i className="fas fa-times ml-2 cancel" onClick={this.handleClickCancel}></i>
                    </div>
            </div>
        </td>
    );
  }
}


export const TableServersRowComponent = props => {
  return (
    <tr>
        <td>{props.serverTitle}</td>
        <InputBoxContainer value={props.serverCPUPrice} objectId={props.serverId}  updateObject={props.serverUpdateCPUPrice} />
        <InputBoxContainer value={props.serverMemoryPrice} objectId={props.serverId}  updateObject={props.serverUpdateMemoryPrice} />
    </tr>
  );
};


export const TableClustersRowComponent = props => {
  return (
    <tr>
        <td>{props.clusterTitle}</td>
        <InputBoxContainer value={props.clusterCPUPrice} objectId={props.clusterId}  updateObject={props.clusterUpdateCPUPrice} />
        <InputBoxContainer value={props.clusterMemoryPrice} objectId={props.clusterId}  updateObject={props.clusterUpdateMemoryPrice} />
    </tr>
  );
};


class TabServersResourcesComponent extends Component {
    render() {
        return (
            <div className="tab-pane fade show active">
                <div className="table-responsive">
                    <table className="table">
                        <TableHeaderComponent />
                        <TableServersBodyContainer />
                    </table>
                </div>
            </div>
        );
    }
}


class TabClustersResourcesComponent extends Component {
    render() {
        return (
            <div className="tab-pane fade show active">
                <div className="table-responsive">
                    <table className="table">
                        <TableHeaderComponent />
                        <TableClustersBodyContainer />
                    </table>
                </div>
            </div>
        );
    }
}


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
