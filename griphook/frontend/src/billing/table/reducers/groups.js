import * as types from "../actionTypes";

const billingTableInitialState = {
  pageItems: [],
  pagesCount: 1,
  pageNumber: 1,
  nextPageExists: false,
  previousPageExists: false,

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
        pageItems: action.data.table_data,
        // TODO: update API and rename pages to pages_count
        // nextPageExists: action.data.next_page_exists,
        // previousPageExists: action.data.previous_page_exists,
        pagesCount: action.data.pages
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

    case types.SET_BILLING_TABLE_PAGE_NUMBER:
      return { ...state, pageNumber: action.pageNumber };

    default:
      return state;
  }
}
