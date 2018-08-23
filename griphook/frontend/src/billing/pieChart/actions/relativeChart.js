import * as types from "../actionTypes";

export const fetchBillingPieChartRelativeDataBegin = () => ({
  type: types.FETCH_BILLING_PIE_CHART_RELATIVE_DATA_BEGIN
});

export const fetchBillingPieChartRelativeDataSuccess = data => ({
  type: types.FETCH_BILLING_PIE_CHART_RELATIVE_DATA_SUCCESS,
  data
});

export const fetchBillingPieChartRelativeDataFailure = error => ({
  type: types.FETCH_BILLING_PIE_CHART_RELATIVE_DATA_FAILURE,
  error
});

export const fetchBillingPieChartRelativeData = options => dispatch => {
  dispatch(fetchBillingPieChartRelativeDataBegin());
  const requesData = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(options)
  };
  const url = new URL(
    "http://localhost:5000/billing/get_pie_chart_relative_data"
  );
  return fetch(url, requesData)
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchBillingPieChartRelativeDataSuccess(json));
      return json;
    })
    .catch(error => dispatch(fetchBillingPieChartRelativeDataFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
