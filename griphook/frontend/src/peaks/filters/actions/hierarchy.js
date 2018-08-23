import * as types from "../actionTypes";

export const fetchFiltersHierarchyBegin = () => ({
  type: types.FETCH_FILTERS_HIERARCHY_BEGIN
});

export const fetchFiltersHierarchySuccess = hierarchy => ({
  type: types.FETCH_FILTERS_HIERARCHY_SUCCESS,
  hierarchy
});

export const fetchFiltersHierarchyFailure = error => ({
  type: types.FETCH_FILTERS_HIERARCHY_FAILURE,
  payload: { error }
});

export const fetchFiltersHierarchy = () => {
  return dispatch => {
    dispatch(fetchFiltersHierarchyBegin());
    return fetch("http://localhost:5000/filters/peaks_hierarchy")
      .then(handleErrors)
      .then(response => response.json())
      .then(json => {
        dispatch(fetchFiltersHierarchySuccess(json));
        return json;
      })
      .catch(error => dispatch(fetchFiltersHierarchyFailure(error)));
  };
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
