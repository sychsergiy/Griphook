import * as types from "../actionTypes";

export const fetchGroupChartDataBegin = () => ({
  type: types.FETCH_GROUP_CHART_DATA_BEGIN
});

export const fetchGroupChartDataSuccess = data => ({
  type: types.FETCH_GROUP_CHART_DATA_SUCCESS,
  data
});

export const fetchGroupChartDataFailure = error => ({
  type: types.FETCH_GROUP_CHART_DATA_FAILURE,
  error
});

export const fetchGroupChartData = options => dispatch => {
  dispatch(fetchGroupChartDataBegin());
  const requesData = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(options)
  };
  return fetch("/billing/get_services_group_chart", requesData)
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchGroupChartDataSuccess(json));
      return json;
    })
    .catch(error => dispatch(fetchGroupChartDataFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
