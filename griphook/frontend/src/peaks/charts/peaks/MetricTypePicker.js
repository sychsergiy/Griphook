import React from "react";
import { connect } from "react-redux";

import { setPeaksChartMetricTypeOption } from "./actions";

import MetricTypePickerComponent from "../metricTypePickerComponent";

const mapStateToProps = state => ({
  currentMetricType: state.peaks.charts.peaksChart.metricType
});

const mapDispatchToProps = dispatch => ({
  setMetricType: metricType => {
    dispatch(setPeaksChartMetricTypeOption(metricType));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(MetricTypePickerComponent);
