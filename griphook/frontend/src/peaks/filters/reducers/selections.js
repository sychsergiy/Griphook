import * as types from "../actionTypes";

const selectedInitialState = {
  clusters: [],
  servers: [],
  servicesGroups: [],
  services: []
};

export function selections(state = selectedInitialState, action) {
  switch (action.type) {
    case types.SELECT_CLUSTER_FILTER:
      return {
        ...state,
        clusters: [...state.clusters, action.clusterID]
      };
    case types.UNSELECT_CLUSTER_FILTER:
      const clusterIndex = state.clusters.indexOf(action.clusterID);
      return {
        ...state,
        clusters: [
          ...state.clusters.slice(0, clusterIndex),
          ...state.clusters.slice(clusterIndex + 1)
        ]
      };
    case types.SELECT_SERVER_FILTER:
      return {
        ...state,
        servers: [...state.servers, action.serverID]
      };
    case types.UNSELECT_SERVER_FILTER:
      const indexOfServerToRemove = state.servers.indexOf(action.serverID);
      return {
        ...state,
        servers: [
          ...state.servers.slice(0, indexOfServerToRemove),
          ...state.servers.slice(indexOfServerToRemove + 1)
        ]
      };
    case types.SELECT_SERVICES_GROUP_FILTER:
      return {
        ...state,
        servicesGroups: [...state.servicesGroups, action.servicesGroupID]
      };
    case types.UNSELECT_SERVICES_GROUP_FILTER:
      const indexOfGroupToRemove = state.servicesGroups.indexOf(
        action.servicesGroupID
      );
      return {
        ...state,
        servicesGroups: [
          ...state.servicesGroups.slice(0, indexOfGroupToRemove),
          ...state.servicesGroups.slice(indexOfGroupToRemove + 1)
        ]
      };
    default:
      return state;
  }
}
