import * as types from "../actionTypes";

const selectedInitialState = {
  projects: [],
  teams: [],
  clusters: [],
  servers: [],
  servicesGroups: []
};

export function selections(state = selectedInitialState, action) {
  switch (action.type) {
    case types.SELECT_BILLING_CLUSTER_FILTER:
      return { ...state, clusters: [...state.clusters, action.clusterID] };
    case types.UNSELECT_BILLING_CLUSTER_FILTER:
      const clusterIndex = state.clusters.indexOf(action.clusterID);
      return {
        ...state,
        clusters: [
          ...state.clusters.slice(0, clusterIndex),
          ...state.clusters.slice(clusterIndex + 1)
        ]
      };
    case types.SELECT_BILLING_SERVER_FILTER:
      return { ...state, servers: [...state.servers, action.serverID] };
    case types.UNSELECT_BILLING_SERVER_FILTER:
      const indexOfServerToRemove = state.servers.indexOf(action.serverID);
      return {
        ...state,
        servers: [
          ...state.servers.slice(0, indexOfServerToRemove),
          ...state.servers.slice(indexOfServerToRemove + 1)
        ]
      };
    case types.SELECT_BILLING_PROJECT_FILTER:
      return { ...state, projects: [...state.projects, action.projectID] };
    case types.UNSELECT_BILLING_PROJECT_FILTER:
      const indexOfProjectToRemove = state.projects.indexOf(action.projectID);
      return {
        ...state,
        projects: [
          ...state.projects.slice(0, indexOfProjectToRemove),
          ...state.projects.slice(indexOfProjectToRemove + 1)
        ]
      };
    default:
      return state;
  }
}
