import React, { Component } from "react";

import ChartOptionsPeackerContainer from "./containers/ChartsOptionsPeacker";
import PeaksChartContainer from "./containers/PeaksChart";
import AverageLoadChartContainer from "./containers/AverageLoadChart";

class PeaksPage extends Component {
  render() {
    return (
      <div className="col-xl-9 col-lg-8 col-sm-12">
        <ChartOptionsPeackerContainer />
        <div className="plot mb-4">
          <div className="col-md-8 offset-md-2">
            <PeaksChartContainer />
          </div>
        </div>

        <div className="plot mb-4">
          <h3 className="text-center mt-5">Средняя нагруженность</h3>
          <div className="col-md-8 offset-md-2">
            <AverageLoadChartContainer />
          </div>
        </div>
      </div>
    );
  }
}

export default PeaksPage;
