import React, { Component } from "react";

import TimeFromPeacker from "./containers/TimeFromPeacker";
import TimeUntilPeacker from "./containers/TimeUntilPeacker";

class MetricOptionsPeaker extends Component {
  render() {
    return (
      <div className="d-flex justify-content-around flex-wrap">
        <div className="">
          <div className="form-group">
            <label>Start date</label>
            <div className="input-group">
              <div className="input-group-prepend d-md-none d-lg-flex">
                <span className="input-group-text">
                  <i className="far fa-calendar-alt text-primary" />
                </span>
              </div>
              <TimeFromPeacker />
            </div>
          </div>
        </div>

        <div className="">
          <div className="form-group">
            <label>End date</label>
            <div className="input-group">
              <TimeUntilPeacker />
              <div className="input-group-append d-md-none d-lg-flex">
                <span className="input-group-text">
                  <i className="far fa-calendar-alt text-primary" />
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default MetricOptionsPeaker;
