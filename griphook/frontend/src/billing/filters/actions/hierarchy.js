import * as types from "../actionTypes";

export const fetchBillingFiltersHierarchyBegin = () => ({
  type: types.FETCH_BILLING_FILTERS_HIERARCHY_BEGIN
});

export const fetchBillingFiltersHierarchySuccess = hierarchy => ({
  type: types.FETCH_BILLING_FILTERS_HIERARCHY_SUCCESS,
  hierarchy
});

export const fetchBillingFiltersHierarchyFailure = error => ({
  type: types.FETCH_BILLING_FILTERS_HIERARCHY_FAILURE,
  payload: { error }
});

export const fetchBillingFiltersHierarchy = () => dispatch => {
  dispatch(fetchBillingFiltersHierarchyBegin());
  return fetch("http://localhost:5000/filters/billing_hierarchy")
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchBillingFiltersHierarchySuccess(json));
      return json;
    })
    .catch(error => dispatch(fetchBillingFiltersHierarchyFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
