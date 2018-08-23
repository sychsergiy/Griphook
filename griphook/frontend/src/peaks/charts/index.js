import React, { Fragment, Component } from "react";

import PeaksChartContainer from "./peaks/index";
import AverageLoadChartContainer from "./averageLoad/index";

import AverageLoadChartMetricTypeContainer from "./averageLoad/MetricTypePeacker";
import PeaksChartMetricTypeContainer from "./peaks/MetricTypePeacker";

// TODO: component for chart block wrapper
// TODO: refactor this component
// TODO: also refactor charts folders (create containers and components folders)

const ChartsComponent = props => (
  <Fragment>
    <div className="peak-chart-block mt-5 ">
      <div className="card border-primary mb-3">
        <h4 className="card-header">
          <i className="far fa-chart-bar mr-2" />Peaks chart
        </h4>
        <div className="card-body">
          <div className="row">
            <div className="col-12">
              <h4 className="card-title float-left text-muted">
                Chart for:
                <span className="ml-2 text-primary">adv-some-service</span>
              </h4>
              <PeaksChartMetricTypeContainer />
            </div>
            <div className="peak-chart-outer col-12 col-md-11 col-lg-10 mx-auto">
              <PeaksChartContainer />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div className="peak-chart-block mt-5 ">
      <div className="card border-primary mb-3">
        <h4 className="card-header">
          <i className="far fa-chart-bar mr-2" />Average chart
        </h4>
        <div className="card-body">
          <div className="row">
            <div className="col-12">
              <h4 className="card-title float-left text-muted">
                Chart for:
                <span className="ml-2 text-primary">adv-some-service</span>
              </h4>
              <AverageLoadChartMetricTypeContainer />
            </div>

            <div className="peak-chart-outer col-12 col-md-11 col-lg-10 mx-auto">
              <AverageLoadChartContainer />
            </div>
          </div>
        </div>
      </div>
    </div>
  </Fragment>
);

export default ChartsComponent;
