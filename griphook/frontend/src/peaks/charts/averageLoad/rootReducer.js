import * as types from "./actionTypes";

import { metricTypes } from "../../../common/constants";

const averageLoadChartInitialState = {
  data: {},
  loading: false,
  error: null,
  metricType: metricTypes.memory
};

export function averageLoadChart(state = averageLoadChartInitialState, action) {
  switch (action.type) {
    case types.FETCH_AVERAGE_LOAD_CHART_DATA_BEGIN:
      return {
        ...state,
        loading: true,
        error: null
      };

    case types.FETCH_AVERAGE_LOAD_CHART_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        data: action.data
      };

    case types.FETCH_AVERAGE_LOAD_CHART_DATA_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error
      };

    case types.SET_AVERAGE_LOAD_CHART_METRIC_TYPE_OPTION:
      return {
        ...state,
        metricType: action.metricType
      };
    default:
      return state;
  }
}
