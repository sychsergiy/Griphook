import React, { Component } from "react";
import { connect } from "react-redux";

import ServicesChartComponent from "../components/servicesChart";

import {
  fetchGroupChartData,
  setGroupChartMetricType
} from "../actions/groupChart";

import { metricTypes } from "../../../common/constants";
import { isEquivalent } from "../../../common/utils";

class ServicesChartContainer extends Component {
  componentDidMount() {
    this.props.fetchChartData(this.props.requestOptions);
  }

  componentWillReceiveProps(nextProps) {
    if (!isEquivalent(nextProps.requestOptions, this.props.requestOptions)) {
      this.props.fetchChartData(nextProps.requestOptions);
    }
  }

  constructChartData(chartData) {
    let constructedData = {
      labels: chartData.timeline,
      datasets: [
        {
          label: this.props.requestOptions.metric_type,
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

  render() {
    const chartData = this.props.chartData
      ? this.constructChartData(this.props.chartData)
      : {};

    return (
      <ServicesChartComponent
        setMetricType={this.props.setMetricType}
        metricType={this.props.requestOptions.metric_type}
        chartData={chartData}
        loading={this.props.loading}
        error={this.props.error}
      />
    );
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    metric_type: state.billing.table.groupChart.metricType,
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
  },
  setMetricType: metricType => {
    dispatch(setGroupChartMetricType(metricType));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServicesChartContainer);
