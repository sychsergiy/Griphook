import React, {Component} from "react";
import {NavLink} from "react-router-dom";

class SettingsMenuComponent extends Component {
  render() {
    const style = {
      width: 270
    }
    return (<ul className="nav nav-pills flex-column mt-4" style={style}>
      <li className="nav-item">
        <NavLink to="/settings/tasks" className="nav-link" activeClassName="active">
          <i className="fas fa-tasks mr-2"></i>Tasks control</NavLink>
      </li>
      <li className="nav-item">
        <NavLink to="/settings/resources" className="nav-link" activeClassName="active">
          <i className="far fa-hdd mr-2"></i>Resources control</NavLink>
      </li>
    </ul>);
  }
}

export default SettingsMenuComponent;
