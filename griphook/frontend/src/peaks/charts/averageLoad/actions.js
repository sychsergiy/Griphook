import * as types from "./actionTypes";

export const fetchAverageLoadChartDataBegin = () => ({
  type: types.FETCH_AVERAGE_LOAD_CHART_DATA_BEGIN
});

export const fetchAverageLoadChartDataSuccess = data => ({
  type: types.FETCH_AVERAGE_LOAD_CHART_DATA_SUCCESS,
  data
});

export const fetchAverageLoadChartDataFailure = error => ({
  type: types.FETCH_AVERAGE_LOAD_CHART_DATA_FAILURE,
  error
});

export const fetchAverageLoadChartData = options => dispatch => {
  dispatch(fetchAverageLoadChartDataBegin());
  const url = new URL("http://localhost:5000/average_load/chart_data");
  let data = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(options)
  };
  return fetch(url, data)
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchAverageLoadChartDataSuccess(json));
      return json;
    })
    .catch(error => dispatch(fetchAverageLoadChartDataFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

export const setAverageLoadChartMetricTypeOption = metricType => ({
  type: types.SET_AVERAGE_LOAD_CHART_METRIC_TYPE_OPTION,
  metricType
});
