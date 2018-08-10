import * as types from "../actionTypes";

import moment from "moment";

import { metricTypes } from "../common";

const chartsOptionsInitialState = {
  timeFrom: moment(),
  timeUntil: moment(),
  metricType: metricTypes[0]
};

export function chartsOptions(state = chartsOptionsInitialState, action) {
  switch (action.type) {
    case types.SET_TIME_FROM_OPTION:
      return { ...state, timeFrom: action.date };
    case types.SET_TIME_UNTIL_OPTION:
      return { ...state, timeUntil: action.date };
    case types.SET_METRIC_TYPE_OPTION:
      return { ...state, metricType: action.metricType };
    default:
      return state;
  }
}
