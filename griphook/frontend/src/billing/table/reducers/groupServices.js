import * as types from "../actionTypes";

const groupServicesInitialState = {
  items: [],
  loading: false,
  error: null
};

export function groupServices(state = groupServicesInitialState, action) {
  switch (action.type) {
    case types.FETCH_GROUP_SERVICES_DATA_BEGIN:
      return {
        ...state,
        loading: true,
        error: null
      };

    case types.FETCH_GROUP_SERVICES_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        items: action.items
      };

    case types.FETCH_GROUP_SERVICES_DATA_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error
      };

    default:
      return state;
  }
}
