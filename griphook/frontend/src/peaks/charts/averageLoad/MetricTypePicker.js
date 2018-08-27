import React from "react";
import { connect } from "react-redux";

import { setAverageLoadChartMetricTypeOption } from "./actions";

import MetricTypePickerComponent from "../metricTypePickerComponent";

const mapStateToProps = state => ({
  currentMetricType: state.peaks.charts.averageLoadChart.metricType
});

const mapDispatchToProps = dispatch => ({
  setMetricType: metricType => {
    dispatch(setAverageLoadChartMetricTypeOption(metricType));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(MetricTypePickerComponent);
