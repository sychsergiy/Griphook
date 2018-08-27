import React from "react";
import { connect } from "react-redux";

import 'react-datepicker/dist/react-datepicker.css';

import ChartsOptionsPickerComponent from "./components/chartsOptionsPicker";

import {
  setTimeFromOption,
  setTimeUntilOption,
  setTimeStepOption
} from "./actions";

const mapStateToProps = state => ({
  timeFrom: state.peaks.chartsOptions.timeFrom,
  timeUntil: state.peaks.chartsOptions.timeUntil,
  currentTimeStep: state.peaks.chartsOptions.timeStep
});

const mapDispatchToProps = dispatch => ({
  onChangeTimeFrom: date => {
    dispatch(setTimeFromOption(date));
  },
  onChangeTimeUntil: date => {
    dispatch(setTimeUntilOption(date));
  },
  onTimeStepChange: timeStep => {
    dispatch(setTimeStepOption(timeStep));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ChartsOptionsPickerComponent);
