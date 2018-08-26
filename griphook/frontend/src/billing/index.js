import React, { Component } from "react";

import BillingFiltersContainer from "./filters/index";
import MetricOptionsPeaker from "./options/index";
import PieChartContainer from "./pieChart/index";
import BillingTable from "./table/index";

class BillingPage extends Component {
  render() {
    return (
      <div className="container-fluid">
        <div className="d-flex flex-wrap flex-md-nowrap">
          <BillingFiltersContainer />

          <div class="flex-grow-1 mx-md-1 mx-lg-4">
            <div class="time-filter mt-2 mb-5">
              <div class="card border-primary mb-3">
                <div class="card-body">
                  <MetricOptionsPeaker />
                </div>
              </div>
            </div>

            <div class="pie-charts mt-2 mb-5">
              <div class="card border-primary mb-3">
                <h5 class="card-header">
                  <i class="fas fa-chart-pie mr-2" />
                  Pie Charts
                </h5>
                <PieChartContainer />
              </div>
            </div>

            <div className="col-xl-9 col-lg-8 col-sm-12">
              <BillingTable />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default BillingPage;
