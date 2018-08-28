import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchBillingPieChartAbsoluteData } from "../actions/absoluteChart";

import { isEquivalent } from "../../../common/utils";

import { Pie } from "react-chartjs-2";

import AbsoluteChartComponent from "../components/absoluteChart";

class AbsolutePieChartContainer extends Component {
  componentDidMount() {
    let options = {
      ...this.props.requestOptions,
      metric_type: this.props.metricType
    };
    this.props.fetchChartData(options);
  }

  componentWillReceiveProps(nextProps) {
    // TODO: set default target_type to "all"
    // but for the first check if other request still working!
    const isRefetchNeccessary =
      !isEquivalent(nextProps.requestOptions, this.props.requestOptions) ||
      nextProps.metricType !== this.props.metricType;
    if (isRefetchNeccessary) {
      // TODO: send metric_type to redux?
      let options = {
        ...nextProps.requestOptions,
        metric_type: nextProps.metricType
      };
      this.props.fetchChartData(options);
    }
  }

  render() {
    if (this.props.loading) {
      return <div>Loading ...</div>;
    }
    if (this.props.error) {
      return <div>{this.props.error.toString()}</div>;
    }

    const chartData = this.props.chartData
      ? {
          labels: this.props.chartData.labels,
          datasets: [
            {
              data: this.props.chartData.values,
              backgroundColor: ["#f39c12", "#e74c3c"]
            }
          ]
        }
      : { labels: [], datasets: [] };
    return <AbsoluteChartComponent chartData={chartData} />;
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.billing.options.timeFrom.format("YYYY-MM-DD"),
    time_until: state.billing.options.timeUntil.format("YYYY-MM-DD"),
    target_ids: state.billing.options.targetIDs,
    target_type: state.billing.options.targetType
  },
  chartData: state.billing.pieCharts.absoluteChart.data,
  error: state.billing.pieCharts.absoluteChart.error,
  loading: state.billing.pieCharts.absoluteChart.loading
});
const mapDispatchToProps = dispatch => ({
  fetchChartData: options => {
    dispatch(fetchBillingPieChartAbsoluteData(options));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AbsolutePieChartContainer);
