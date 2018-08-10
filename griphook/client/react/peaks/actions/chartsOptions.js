import * as types from "../actionTypes";

export const setTimeFromOption = date => ({
  type: types.SET_TIME_FROM_OPTION,
  date
});

export const setTimeUntilOption = date => ({
  type: types.SET_TIME_UNTIL_OPTION,
  date
});

export const setMetricTypeOption = metricType => ({
  type: types.SET_METRIC_TYPE_OPTION,
  metricType
});
