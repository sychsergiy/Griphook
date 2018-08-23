import * as types from "../actionTypes";

export const fetchGroupServicesDataBegin = () => ({
  type: types.FETCH_GROUP_SERVICES_DATA_BEGIN
});

export const fetchGroupServicesDataSuccess = items => ({
  type: types.FETCH_GROUP_SERVICES_DATA_SUCCESS,
  items
});

export const fetchGroupServicesDataFailure = error => ({
  type: types.FETCH_GROUP_SERVICES_DATA_FAILURE,
  error
});

export const fetchGroupServicesData = options => dispatch => {
  dispatch(fetchGroupServicesDataBegin());
  let data = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(options)
  };
  const url = new URL(
    "http://localhost:5000/billing/get_service_group_metrics"
  );
  return fetch(url, data)
    .then(handleErrors)
    .then(response => response.json())
    .then(json => {
      dispatch(fetchGroupServicesDataSuccess(json));
      return json;
    })
    .catch(error => dispatch(fetchhGroupServicesDataFailure(error)));
};

function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
