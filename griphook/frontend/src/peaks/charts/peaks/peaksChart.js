import React from "react";

import { Bar } from "react-chartjs-2";

const PeaksChartComponent = props => {
  const chartOptions = {
    scales: { xAxes: [{ gridLines: { offsetGridLines: false } }] }
  };

  return <Bar data={props.data} options={chartOptions} />;
};

export default PeaksChartComponent;
