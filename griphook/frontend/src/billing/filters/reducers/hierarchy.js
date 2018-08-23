import * as types from "../actionTypes";

const hierarchyInitialState = {
  projects: [],
  teams: [],
  clusters: [],
  servers: [],
  servicesGroups: [],
  services: [],
  loading: false,
  error: null
};

export function hierarchy(state = hierarchyInitialState, action) {
  switch (action.type) {
    case types.FETCH_BILLING_FILTERS_HIERARCHY_BEGIN:
      return {
        ...state,
        loading: true,
        error: null
      };

    case types.FETCH_BILLING_FILTERS_HIERARCHY_SUCCESS:
      return {
        ...state,
        loading: false,
        teams: action.hierarchy.teams,
        projects: action.hierarchy.projects,
        clusters: action.hierarchy.clusters,
        servers: action.hierarchy.servers,
        servicesGroups: action.hierarchy.services_groups,
        services: action.hierarchy.services
      };

    case types.FETCH_BILLING_FILTERS_HIERARCHY_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload.error
      };

    default:
      return state;
  }
}
