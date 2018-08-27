import React, { Component } from "react";

import TimeFromPeacker from "./containers/TimeFromPeacker";
import TimeUntilPeacker from "./containers/TimeUntilPeacker";

class MetricOptionsPeaker extends Component {
  render() {
    return (
      <div className="row">
        <div className="col-md-6">
          <TimeFromPeacker />
        </div>
        <div className="col-md-6">
          <TimeUntilPeacker />
        </div>
      </div>
    );
  }
}

export default MetricOptionsPeaker;
