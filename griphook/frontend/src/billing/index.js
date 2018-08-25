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
          <div className="col-xl-9 col-lg-8 col-sm-12">
            <MetricOptionsPeaker />
            <PieChartContainer />
            <BillingTable />
          </div>
        </div>
      </div>
    );
  }
}

export default BillingPage;
