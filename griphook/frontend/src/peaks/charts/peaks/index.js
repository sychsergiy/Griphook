import React, { Component } from "react";
import { connect } from "react-redux";

import PeaksChartComponent from "./peaksChart";

import { fetchPeaksChartData } from "./actions";

import { isEquivalent } from "../../../common/utils";
import { Spinner } from "../../../common/spinner";

class PeaksChartContainer extends Component {
  componentWillReceiveProps(nextProps) {
    const isRefetchNeeded =
      !isEquivalent(nextProps.requestOptions, this.props.requestOptions) &&
      nextProps.requestOptions.target_id; // target ID must be not null
    if (isRefetchNeeded) {
      this.props.fetchChartdata(nextProps.requestOptions);
    }
  }

  constructChartData(chartData) {
    if (!chartData.timeline) {
      return { labels: [], datasets: [] };
    }
    let constructedData = {
      labels: [...chartData.timeline, ""],
      datasets: [
        {
          label: chartData.metric_type,
          data: [...chartData.values, 0],
          backgroundColor: "#041558"
        }
      ]
    };
    return constructedData;
  }

  render() {
    if (this.props.loading) {
      return <Spinner />;
    }
    let data = this.constructChartData(this.props.chartData);

    return <PeaksChartComponent data={data} />;
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.peaks.chartsOptions.timeFrom.format("YYYY-MM-DD"),
    time_until: state.peaks.chartsOptions.timeUntil.format("YYYY-MM-DD"),
    metric_type: state.peaks.charts.peaksChart.metricType,
    target_id: state.peaks.chartsOptions.targetID,
    target_type: state.peaks.chartsOptions.targetType,
    step: state.peaks.chartsOptions.timeStep
  },

  error: state.peaks.charts.peaksChart.error,
  loading: state.peaks.charts.peaksChart.loading,
  chartData: state.peaks.charts.peaksChart.data
});

const mapDispatchToProps = dispatch => ({
  fetchChartdata: options => {
    dispatch(fetchPeaksChartData(options));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(PeaksChartContainer);
