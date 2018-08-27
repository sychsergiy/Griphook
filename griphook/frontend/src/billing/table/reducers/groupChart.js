import * as types from "../actionTypes";

const groupServicesInitialState = {
  data: {},
  loading: false,
  error: null
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

    default:
      return state;
  }
}
