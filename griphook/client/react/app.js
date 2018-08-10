import React, { Component } from "react";
import { connect } from "react-redux";

import Filters from "./filters";

import PeaksPage from "./peaks";

class App extends Component {
  constructor(props) {
    super();
  }

  render() {
    return (
      <div id="page-content">
        <div className="container-fluid">
          <div className="row">
            <Filters />
            <PeaksPage />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
