import React, { Component } from "react";

import DatePicker from "react-datepicker";

import MetricTypePeackerComponent from "./metricTypePeacker";

const ChartsOptionsPeackerComponent = props => (
  <div className="row">
    <div className="col-md-4">
      <DatePicker selected={props.timeFrom} onChange={props.onChangeTimeFrom} />
    </div>
    <div className="col-md-4">
      <DatePicker
        selected={props.timeUntil}
        onChange={props.onChangeTimeUntil}
      />
    </div>

    <div className="col-md-4">
      <MetricTypePeackerComponent
        currentMetricType={props.currentMetricType}
        onChangeMetricType={props.onChangeMetricType}
      />
    </div>
  </div>
);

export default ChartsOptionsPeackerComponent;
