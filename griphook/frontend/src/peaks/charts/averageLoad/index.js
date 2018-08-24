import React, { Component } from "react";
import { connect } from "react-redux";

import AverageLoadChartComponent from "./averageLoadChart";

import { isEquivalent } from "../../../common/utils";

import { fetchAverageLoadChartData } from "./actions";

class AverageLoadChartContainer extends Component {
  componentWillReceiveProps(nextProps) {
    const isRefetchNeeded =
      !isEquivalent(nextProps.requestOptions, this.props.requestOptions) &&
      nextProps.requestOptions.target_id; // target ID must be not null
    if (isRefetchNeeded) {
      this.props.fetchChartdata(nextProps.requestOptions);
    }
  }

  constructChartData(chartData) {
    const ROOT_BAR_COLOR = "#1b665c",
      CHILD_BAR_COLOR = "#38c9b6";
    let constructedData = {};

    if (chartData.hasOwnProperty("target_label")) {
      let labels = [chartData.target_label, ...chartData.children_labels];
      let data = [chartData.target_value, ...chartData.children_values];

      let backgroundColor = data.map(
        (value, index) => (index === 0 ? ROOT_BAR_COLOR : CHILD_BAR_COLOR)
      );
      let datasets = [{ label: chartData.metric_type, data, backgroundColor }];
      constructedData = { datasets, labels };
    }

    return constructedData;
  }

  render() {
    if (this.props.loading) {
      return <div>Loading ...</div>;
    }

    let options = {
      scales: { xAxes: [{ gridLines: { offsetGridLines: false } }] }
    };
    let data = this.constructChartData(this.props.chartData);

    return <AverageLoadChartComponent data={data} options={options} />;
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.peaks.chartsOptions.timeFrom.format("YYYY-MM-DD"),
    time_until: state.peaks.chartsOptions.timeUntil.format("YYYY-MM-DD"),
    metric_type: state.peaks.charts.averageLoadChart.metricType,
    target_id: state.peaks.chartsOptions.targetID,
    target_type: state.peaks.chartsOptions.targetType
  },

  error: state.peaks.charts.averageLoadChart.error,
  loading: state.peaks.charts.averageLoadChart.loading,
  chartData: state.peaks.charts.averageLoadChart.data
});

const mapDispatchToProps = dispatch => ({
  fetchChartdata: options => {
    dispatch(fetchAverageLoadChartData(options));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(AverageLoadChartContainer);
