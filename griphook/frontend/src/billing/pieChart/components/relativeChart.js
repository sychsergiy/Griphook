import React from "react";
import { Pie } from "react-chartjs-2";

const RelativePieChartComponent = props => {
  const options = {
    legend: {
      display: false
    },
    tooltips: {
      callbacks: {
        label: function(tooltipItem, data) {
          let dataset = data.datasets[tooltipItem.datasetIndex];
          let total = dataset.data.reduce(
            (previousValue, currentValue, currentIndex, array) =>
              previousValue + currentValue
          );
          let currentValue = dataset.data[tooltipItem.index];
          let percentage = Math.floor((currentValue / total) * 100 + 0.5);
          let currentLabel = data.labels[tooltipItem.index];
          return currentLabel + ": " + percentage + "%";
        }
      }
    }
  };
  return <Pie data={props.chartData} options={options} />;
};

export default RelativePieChartComponent;
