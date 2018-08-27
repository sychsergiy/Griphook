import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchBillingPieChartRelativeData } from "../actions/relativeChart";

import { isEquivalent } from "../../../common/utils";
import { metricTypes } from "../../../common/constants";

import { Pie } from "react-chartjs-2";

import RelativePieChartComponent from "../components/relativeChart";

class RelativePieChartContainer extends Component {
  componentDidMount() {
    let options = {
      ...this.props.requestOptions,
      metric_type: this.props.metricType
    };
    this.props.fetchChartData(options);
  }

  componentWillReceiveProps(nextProps) {
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
              backgroundColor: "#3860a0"
            }
          ]
        }
      : { labels: [], datasets: [] };
    return <RelativePieChartComponent chartData={chartData} />;
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.billing.options.timeFrom.format("YYYY-MM-DD"),
    time_until: state.billing.options.timeUntil.format("YYYY-MM-DD"),
    target_ids: state.billing.options.targetIDs,
    target_type: state.billing.options.targetType
  },
  chartData: state.billing.pieCharts.relativeChart.data,
  error: state.billing.pieCharts.relativeChart.error,
  loading: state.billing.pieCharts.relativeChart.loading
});
const mapDispatchToProps = dispatch => ({
  fetchChartData: options => {
    dispatch(fetchBillingPieChartRelativeData(options));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(RelativePieChartContainer);
