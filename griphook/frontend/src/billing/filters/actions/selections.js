import * as types from "../actionTypes";

export const selectClusterFilter = clusterID => ({
  type: types.SELECT_BILLING_CLUSTER_FILTER,
  clusterID
});

export const unSelectClusterFilter = clusterID => ({
  type: types.UNSELECT_BILLING_CLUSTER_FILTER,
  clusterID
});

export const selectServerFilter = serverID => ({
  type: types.SELECT_BILLING_SERVER_FILTER,
  serverID
});

export const unSelectServerFilter = serverID => ({
  type: types.UNSELECT_BILLING_SERVER_FILTER,
  serverID
});

export const selectProjectFilter = projectID => ({
  type: types.SELECT_BILLING_PROJECT_FILTER,
  projectID
});

export const unSelectProjectFilter = projectID => ({
  type: types.UNSELECT_BILLING_PROJECT_FILTER,
  projectID
});
