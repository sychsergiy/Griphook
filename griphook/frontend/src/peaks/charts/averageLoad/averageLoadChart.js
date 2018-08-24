import React, { Component } from "react";

import { HorizontalBar } from "react-chartjs-2";

const AverageLoadChartComponent = props => (
  <HorizontalBar data={props.data} options={props.options} />
);

export default AverageLoadChartComponent;
