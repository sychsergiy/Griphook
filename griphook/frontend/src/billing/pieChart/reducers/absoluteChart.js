import * as types from "../actionTypes";

const absoluteChartInitialState = {
  data: null,
  loading: false,
  error: null
};

export function absoluteChart(state = absoluteChartInitialState, action) {
  switch (action.type) {
    case types.FETCH_BILLING_PIE_CHART_ABSOLUTE_DATA_BEGIN:
      return {
        ...state,
        loading: true,
        error: null
      };

    case types.FETCH_BILLING_PIE_CHART_ABSOLUTE_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        data: action.data
      };

    case types.FETCH_BILLING_PIE_CHART_ABSOLUTE_DATA_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error
      };

    default:
      return state;
  }
}
