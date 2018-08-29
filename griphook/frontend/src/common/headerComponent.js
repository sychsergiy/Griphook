import React, { Component } from "react";

import {Link, NavLink} from "react-router-dom";

const HeaderComponent = () => (
  <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
    <Link to="/" className="navbar-brand">
      <i className="fas fa-coins mr-2" />
      Griphook
    </Link>
    <button
      className="navbar-toggler"
      type="button"
      data-toggle="collapse"
      data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span className="navbar-toggler-icon" />
    </button>

    <div className="collapse navbar-collapse" id="navbarSupportedContent">
      <ul className="navbar-nav mr-auto">
        <li className="nav-item">
          <Link to="/billing" className="nav-link">
            Billing
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/peaks" className="nav-link">
            Peaks
          </Link>
        </li>
      </ul>
      <ul className="navbar-nav ml-auto">
         <li className="nav-item">
            <Link to="/settings/tasks" className="nav-link">
                <i className="fas fa-wrench mr-1" />
                Settings
            </Link>
         </li>
      </ul>
    </div>
  </nav>
);

export default HeaderComponent;




        // {/*<li className="nav-item active">*/}


        // {/*</li>*/}
