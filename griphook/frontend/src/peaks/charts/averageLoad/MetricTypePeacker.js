import React, { Component } from "react";
import { connect } from "react-redux";

import { setAverageLoadChartMetricTypeOption } from "./actions";

import MetricTypePeackerComponent from "../metricTypePeackerComponent";

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
)(MetricTypePeackerComponent);
