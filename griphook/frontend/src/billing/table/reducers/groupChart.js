import * as types from "../actionTypes";

import { metricTypes } from "../../../common/constants";

const groupServicesInitialState = {
  data: null,
  loading: false,
  error: null,
  metricType: metricTypes.memory
};

export function groupChart(state = groupServicesInitialState, action) {
  switch (action.type) {
    case types.FETCH_GROUP_CHART_DATA_BEGIN:
      return {
        ...state,
        loading: true,
        error: null
      };

    case types.FETCH_GROUP_CHART_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        data: action.data
      };

    case types.FETCH_GROUP_CHART_DATA_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error
      };

    case types.SET_GROUP_CHART_METRIC_TYPE:
      return {
        ...state,
        metricType: action.metricType
      };

    default:
      return state;
  }
}
