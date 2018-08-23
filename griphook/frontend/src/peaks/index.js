import React, { Component } from "react";

import ChartOptionsPeackerContainer from "./options/index";
import ChartsComponent from "./charts/index";

import PeaksFiltersContainer from "./filters/index";

const PeaksPage = props => (
  <div className="container-fluid">
    <div className="d-flex flex-wrap flex-md-nowrap">
      <PeaksFiltersContainer />

      <div className="flex-grow-1 mx-md-1 mx-lg-4">
        <div className="time-filter mt-2">
          <div className="card border-primary">
            <div className="card-body">
              <h4 className="card-title text-center">Time filter</h4>
              <ChartOptionsPeackerContainer />
            </div>
          </div>
        </div>
        <ChartsComponent />
      </div>
    </div>
  </div>
);

export default PeaksPage;
