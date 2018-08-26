import React, { Component } from "react";

import BillingFiltersContainer from "./filters/index";
import MetricOptionsPeaker from "./options/index";
import PieChartContainer from "./pieChart/index";
import BillingTable from "./table/index";

import "./main.css";

class BillingPage extends Component {
  render() {
    return (
      <div className="container-fluid">
        <div className="d-flex flex-wrap flex-md-nowrap">
          <BillingFiltersContainer />

          <div className="flex-grow-1 mx-md-1 mx-lg-4">
            <div className="time-filter mt-2 mb-5">
              <div className="card border-primary mb-3">
                <div className="card-body">
                  <MetricOptionsPeaker />
                </div>
              </div>
            </div>

            <div className="pie-charts mt-2 mb-5">
              <div className="card border-primary mb-3">
                <h5 className="card-header">
                  <i className="fas fa-chart-pie mr-2" />
                  Pie Charts
                </h5>
                <PieChartContainer />
              </div>
            </div>
            <BillingTable />
          </div>
        </div>
      </div>
    );
  }
}

export default BillingPage;
