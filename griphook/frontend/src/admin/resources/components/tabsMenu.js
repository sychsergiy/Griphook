import React from "react";
import {NavLink} from "react-router-dom";


export const TabsMenuComponent = () => {
  return (
        <ul className="nav nav-tabs">
            <li className="nav-item">
                <NavLink to="/settings/resources/clusters" className="nav-link" activeClassName="active">
                    <i className="fas fa-th-large mr-2"></i>
                    Clusters
                </NavLink>
            </li>
            <li className="nav-item">
                <NavLink to="/settings/resources/servers" className="nav-link" activeClassName="active">
                    <i className="fas fa-server mr-2"></i>
                    Servers
                </NavLink>
            </li>
        </ul>
  );
};
