import * as types from "../actionTypes";

export const selectClusterFilter = clusterID => ({
  type: types.SELECT_CLUSTER_FILTER,
  clusterID
});

export const unselectClusterFilter = clusterID => ({
  type: types.UNSELECT_CLUSTER_FILTER,
  clusterID
});

export const selectServerFilter = serverID => ({
  type: types.SELECT_SERVER_FILTER,
  serverID
});

export const unselectServerFilter = serverID => ({
  type: types.UNSELECT_SERVER_FILTER,
  serverID
});

export const selectServicesGroupFilter = servicesGroupID => ({
  type: types.SELECT_SERVICES_GROUP_FILTER,
  servicesGroupID
});

export const unselectServicesGroupFilter = servicesGroupID => ({
  type: types.UNSELECT_SERVICES_GROUP_FILTER,
  servicesGroupID
});
