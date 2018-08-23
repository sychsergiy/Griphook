import React from "react";

import { metricTypes } from "../../common/constants";

const MetricTypePeackerComponent = props => (
  <div className="form-group float-right">
    <div
      className="custom-control custom-radio"
      onClick={e => props.setMetricType(metricTypes.cpu)}
    >
      <input
        type="radio"
        value={metricTypes.cpu}
        className="custom-control-input"
        checked={metricTypes.cpu === props.currentMetricType}
        onChange={e => {
          console.log("onChange working again");
        }}
      />
      <label className="custom-control-label">{metricTypes.cpu}</label>
    </div>
    <div
      className="custom-control custom-radio"
      onClick={e => props.setMetricType(metricTypes.memory)}
    >
      <input
        type="radio"
        value={metricTypes.memory}
        checked={metricTypes.memory === props.currentMetricType}
        className="custom-control-input"
        onChange={e => {
          console.log("onChange working again");
        }}
      />
      <label className="custom-control-label">{metricTypes.memory}</label>
    </div>
  </div>
);

export default MetricTypePeackerComponent;
