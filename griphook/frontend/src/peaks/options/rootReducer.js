import * as types from "./actionTypes";

import moment from "moment";

import { metricTypes, INTERVALS } from "../../common/constants";

const chartsOptionsInitialState = {
  timeFrom: moment().subtract(3, "months"),
  timeUntil: moment(),
  timeStep: INTERVALS[2].value,
  targetID: null,
  targetType: ""
};

export function chartsOptions(state = chartsOptionsInitialState, action) {
  switch (action.type) {
    case types.SET_TIME_FROM_OPTION:
      return { ...state, timeFrom: action.date };
    case types.SET_TIME_UNTIL_OPTION:
      return { ...state, timeUntil: action.date };
    case types.SET_TIME_STEP_OPTION:
      return { ...state, timeStep: action.timeStep };
    case types.SELECT_PEAKS_TARGET:
      return {
        ...state,
        targetID: action.targetID,
        targetType: action.targetType
      };
    default:
      return state;
  }
}
