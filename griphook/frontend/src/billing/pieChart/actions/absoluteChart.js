import * as types from "../actionTypes";

export const fetchBillingPieChartAbsoluteDataBegin = () => ({
  type: types.FETCH_BILLING_PIE_CHART_ABSOLUTE_DATA_BEGIN
});

export const fetchBillingPieChartAbsoluteDataSuccess = data => ({
  type: types.FETCH_BILLING_PIE_CHART_ABSOLUTE_DATA_SUCCESS,
  data
});

export const fetchBillingPieChartAbsoluteDataFailure = error => ({
  type: types.FETCH_BILLING_PIE_CHART_ABSOLUTE_DATA_FAILURE,
  error
});

export const fetchBillingPieChartAbsoluteData = options => dispatch => {
  dispatch(fetchBillingPieChartAbsoluteDataBegin());
  const requesData = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(options)
  };
  return fetch("/api/billing/get_pie_chart_absolute_data", requesData)
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchBillingPieChartAbsoluteDataSuccess(json));
      return json;
    })
    .catch(error => dispatch(fetchBillingPieChartAbsoluteDataFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
