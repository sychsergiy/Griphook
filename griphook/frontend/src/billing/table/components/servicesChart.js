import React, { Fragment } from "react";

import { metricTypes } from "../../../common/constants";

import { Spinner } from "../../../common/spinner";

import { Line } from "react-chartjs-2";

const LineChart = props => {
  let chartOptions = {
    scales: {
      xAxes: [{ type: "time", distribution: "series" }]
    }
  };

  return <Line data={props.chartData} options={chartOptions} />;
};

const ServicesChartComponent = props => {
  if (props.loading) {
    return <Spinner />;
  }

  if (props.error) {
    return props.error.toString();
  }
  return (
    <Fragment>
      <div className="metric-type-filter mt-5 mb-2 d-flex flex-row">
        <div
          className="custom-control custom-radio mx-3"
          onClick={e => props.setMetricType(metricTypes.cpu)}
        >
          <input
            type="radio"
            className="custom-control-input"
            value={metricTypes.cpu}
            checked={props.metricType === metricTypes.cpu}
            onChange={e => {}}
          />
          <label className="custom-control-label">CPU</label>
        </div>
        <div
          className="custom-control custom-radio mx-3"
          onClick={e => props.setMetricType(metricTypes.memory)}
        >
          <input
            type="radio"
            className="custom-control-input"
            value={metricTypes.memory}
            checked={props.metricType === metricTypes.memory}
            onChange={e => {}}
          />
          <label className="custom-control-label">Memory</label>
        </div>
      </div>
      <LineChart chartData={props.chartData} />
    </Fragment>
  );
};

export default ServicesChartComponent;
