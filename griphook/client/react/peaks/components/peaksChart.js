import React, { Component } from "react";

import { Bar } from "react-chartjs-2";

const PeaksChartComponent = props => (
  <Bar data={props.data} options={props.options} />
);

export default PeaksChartComponent;
