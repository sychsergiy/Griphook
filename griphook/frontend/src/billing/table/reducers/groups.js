import * as types from "../actionTypes";

const billingTableInitialState = {
  items: [],
  selectedItemID: null,
  loading: false,
  error: null
};

export function groups(state = billingTableInitialState, action) {
  switch (action.type) {
    case types.FETCH_BILLING_TABLE_DATA_BEGIN:
      return {
        ...state,
        loading: true,
        error: null
      };

    case types.FETCH_BILLING_TABLE_DATA_SUCCESS:
      return {
        ...state,
        loading: false,
        items: action.data.table_data
      };

    case types.FETCH_BILLING_TABLE_DATA_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.error
      };

    case types.SELECT_BILLING_TABLE_ROW:
      return {
        ...state,
        selectedItemID: action.servicesGroupID
      };
    case types.UNSELECT_BILLING_TABLE_ROW:
      return {
        ...state,
        selectedItemID: null
      };

    default:
      return state;
  }
}
