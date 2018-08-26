import React, { Component } from "react";

import TimeFromPeacker from "./containers/TimeFromPeacker";
import TimeUntilPeacker from "./containers/TimeUntilPeacker";

class MetricOptionsPeaker extends Component {
  render() {
    return (
      <div class="d-flex justify-content-around flex-wrap">
        <div class="">
          <div class="form-group">
            <label>Start date</label>
            <div class="input-group">
              <div class="input-group-prepend d-md-none d-lg-flex">
                <span class="input-group-text">
                  <i class="far fa-calendar-alt text-primary" />
                </span>
              </div>
              <TimeFromPeacker />
            </div>
          </div>
        </div>

        <div class="">
          <div class="form-group">
            <label for="end-date-input">End date</label>
            <div class="input-group">
              <TimeUntilPeacker />
              <div class="input-group-append d-md-none d-lg-flex">
                <span class="input-group-text">
                  <i class="far fa-calendar-alt text-primary" />
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
