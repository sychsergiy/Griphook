import React, { Component } from "react";
import { connect } from "react-redux";

import { Line } from "react-chartjs-2";

import { fetchGroupChartData } from "../actions/groupChart";

const metricTypes = {
  cpu: "cpu",
  memory: "Memory"
};

class ServicesChartContainer extends Component {
  constructor(props) {
    super();
    this.setMemoryMetricType = this.setMemoryMetricType.bind(this);
    this.setCpuMetricType = this.setCpuMetricType.bind(this);

    this.state = {
      metricType: metricTypes.memory
    };
  }

  componentDidMount() {
    this.props.fetchChartData(this.props.requestOptions);
  }

  constructChartData(chartData, label) {
    let constructedData = {
      labels: chartData.timeline,
      datasets: [
        {
          label: label,
          data: chartData.values,
          fill: false,
          pointRadius: 0,
          lineTension: 0,
          borderWidth: 2
        }
      ]
    };
    return constructedData;
  }
  setCpuMetricType() {
    this.setState({
      metricType: metricTypes.cpu
    });
  }
  setMemoryMetricType() {
    this.setState({
      metricType: metricTypes.memory
    });
  }

  render() {
    if (this.props.loading) {
      return <div> Loading ...</div>;
    }

    if (this.props.error) {
      return this.props.error.toString();
    }
    let { cpu, memory } = this.props.chartData;
    let chartOptions = {
      scales: {
        xAxes: [
          {
            type: "time",
            distribution: "series"
          }
        ]
      }
    };

    let chart = null;
    if (this.state.metricType === metricTypes.memory) {
      chart = memory ? (
        <Line
          data={this.constructChartData(memory, "Memory")}
          options={chartOptions}
        />
      ) : null;
    } else if (this.state.metricType === metricTypes.cpu) {
      chart = cpu ? (
        <Line
          data={this.constructChartData(cpu, "CPU")}
          options={chartOptions}
        />
      ) : null;
    }

    return (
      <div>
        <button onClick={this.setCpuMetricType}>Cpu</button>
        <button onClick={this.setMemoryMetricType}>Memory</button>

        {chart}
      </div>
    );
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.billing.options.timeFrom.format("YYYY-MM-DD"),
    time_until: state.billing.options.timeUntil.format("YYYY-MM-DD"),
    services_group_id: state.billing.table.groups.selectedItemID
  },

  error: state.billing.table.groupChart.error,
  loading: state.billing.table.groupChart.loading,
  chartData: state.billing.table.groupChart.data
});

const mapDispatchToProps = dispatch => ({
  fetchChartData: options => {
    dispatch(fetchGroupChartData(options));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServicesChartContainer);
