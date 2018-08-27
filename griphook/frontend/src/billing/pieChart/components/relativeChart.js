import React from "react";
import { Pie } from "react-chartjs-2";

const RelativePieChartComponent = props => {
  const options = {
    legend: {
      display: false
    }
  };
  return <Pie data={props.chartData} options={options} />;
};

export default RelativePieChartComponent;
