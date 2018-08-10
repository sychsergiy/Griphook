import React, { Component } from "react";
import { connect } from "react-redux";

import AverageLoadChartComponent from "../components/averageLoadChart";

class AverageLoadChartContainer extends Component {
  constructor(props) {
    super();
  }

  mockPeaksChartData() {
    let data = {
      labels: [1, 2, 3, 4, 5, 6, 7],
      values: [10, 45, 100, 6, 12, 255, 25],
      metricType: "user_cpu_percent"
    };
    return data;
  }

  render() {
    let options = {
      scales: { xAxes: [{ gridLines: { offsetGridLines: false } }] }
    };
    let mockedData = this.mockPeaksChartData();

    let data = {
      labels: [...mockedData.labels, ""],
      datasets: [
        {
          label: mockedData.metricType,
          data: [...mockedData.values, 0],
          backgroundColor: "#041558"
        }
      ]
    };

    return <AverageLoadChartComponent data={data} options={options} />;
  }
}

const mapStateToProps = state => ({});

export default connect(mapStateToProps)(AverageLoadChartContainer);
