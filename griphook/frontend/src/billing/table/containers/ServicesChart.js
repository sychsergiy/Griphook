import React, { Component } from "react";
import { connect } from "react-redux";

import ServicesChartComponent from "../components/servicesChart";

import { fetchGroupChartData } from "../actions/groupChart";

import { metricTypes } from "../../../common/constants";

class ServicesChartContainer extends Component {
  constructor(props) {
    super();
    this.setMetricType = this.setMetricType.bind(this);
    this.state = {
      metricType: metricTypes.memory
    };
  }

  componentDidMount() {
    this.props.fetchChartData(this.props.requestOptions);
  }

  constructChartData(chartData) {
    let constructedData = {
      labels: chartData.timeline,
      datasets: [
        {
          label: this.state.metricType,
          data: chartData.values,
          fill: false,
          pointRadius: 0,
          lineTension: 0,
          borderWidth: 2,
          borderColor: "#18bc9ca1"
        }
      ]
    };
    return constructedData;
  }

  setMetricType(metricType) {
    this.setState({ metricType });
  }

  render() {
    if (this.props.loading) {
      return <div> Loading ...</div>;
    }

    if (this.props.error) {
      return this.props.error.toString();
    }

    let { cpu, memory } = this.props.chartData;

    // TODO: separete chart data fetch for each metric type
    let chartData = {};
    if (this.state.metricType === metricTypes.memory) {
      chartData = memory ? this.constructChartData(memory) : {};
    } else if (this.state.metricType === metricTypes.cpu) {
      chartData = cpu ? this.constructChartData(cpu) : {};
    }
    return (
      <ServicesChartComponent
        setMetricType={this.setMetricType}
        metricType={this.state.metricType}
        chartData={chartData}
      />
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
