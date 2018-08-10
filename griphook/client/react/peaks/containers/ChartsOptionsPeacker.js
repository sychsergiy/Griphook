import React, { Component } from "react";
import { connect } from "react-redux";

import ChartsOptionsPeackerComponent from "../components/chartsOptionsPeacker";

import {
  setTimeFromOption,
  setTimeUntilOption,
  setMetricTypeOption
} from "../actions/chartsOptions";

class ChartsOptionsPeacker extends Component {
  constructor(props) {
    super();
    this.onChangeTimeFrom = this.onChangeTimeFrom.bind(this);
    this.onChangeTimeUntil = this.onChangeTimeUntil.bind(this);
    this.onChangeMetricType = this.onChangeMetricType.bind(this);
  }

  onChangeTimeFrom(date) {
    this.props.setTimeFrom(date);
  }

  onChangeTimeUntil(date) {
    this.props.setTimeUntil(date);
  }

  onChangeMetricType(e) {
    this.props.setMetricType(e.target.value);
  }

  render() {
    return (
      <ChartsOptionsPeackerComponent
        timeFrom={this.props.timeFrom}
        onChangeTimeFrom={this.onChangeTimeFrom}
        timeUntil={this.props.timeUntil}
        onChangeTimeUntil={this.onChangeTimeUntil}
        currentMetricType={this.props.metricType}
        onChangeMetricType={this.onChangeMetricType}
      />
    );
  }
}

const mapStateToProps = state => ({
  timeFrom: state.peaks.chartsOptions.timeFrom,
  timeUntil: state.peaks.chartsOptions.timeUntil,
  metricType: state.peaks.chartsOptions.metricType
});

const mapDispatchToProps = dispatch => ({
  setTimeFrom: date => {
    dispatch(setTimeFromOption(date));
  },
  setTimeUntil: date => {
    dispatch(setTimeUntilOption(date));
  },
  setMetricType: metricType => {
    dispatch(setMetricTypeOption(metricType));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ChartsOptionsPeacker);
