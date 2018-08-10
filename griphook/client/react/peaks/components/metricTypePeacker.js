import React, { Component } from "react";

import { metricTypes } from "../common";

const MetricTypePeackerComponent = props => (
  <div>
    <input
      onChange={props.onChangeMetricType}
      type="radio"
      value={metricTypes[0]}
      checked={props.currentMetricType === metricTypes[0]}
    />
    <label>Memory</label>
    <input
      onChange={props.onChangeMetricType}
      type="radio"
      value={metricTypes[1]}
      checked={props.currentMetricType === metricTypes[1]}
    />
    <label>CPU</label>
  </div>
);

export default MetricTypePeackerComponent;
