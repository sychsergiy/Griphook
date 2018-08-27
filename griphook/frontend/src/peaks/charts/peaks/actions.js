import * as types from "./actionTypes";

export const fetchPeaksChartDataBegin = () => ({
  type: types.FETCH_PEAKS_CHART_DATA_BEGIN
});

export const fetchPeaksChartDataSuccess = data => ({
  type: types.FETCH_PEAKS_CHART_DATA_SUCCESS,
  data
});

export const fetchPeaksChartDataFailure = error => ({
  type: types.FETCH_PEAKS_CHART_DATA_FAILURE,
  error
});

export const fetchPeaksChartData = options => dispatch => {
  dispatch(fetchPeaksChartDataBegin());
  let data = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(options)
  };
  return fetch("/api/peaks/get_chart", data)
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchPeaksChartDataSuccess(json.data));
      return json.data;
    })
    .catch(error => dispatch(fetchPeaksChartDataFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

export const setPeaksChartMetricTypeOption = metricType => ({
  type: types.SET_PEAKS_CHART_METRIC_TYPE_OPTION,
  metricType
});
