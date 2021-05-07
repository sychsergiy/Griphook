import React, { Component } from "react";

import { Link, NavLink } from "react-router-dom";

const HeaderComponent = () => (
  <nav className="navbar navbar-dark navbar-expand bg-primary">
    <Link to="/" className="navbar-brand">
      <i className="fas fa-coins mr-2" />
      Griphook
    </Link>
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
  </nav>
);

export default HeaderComponent;

