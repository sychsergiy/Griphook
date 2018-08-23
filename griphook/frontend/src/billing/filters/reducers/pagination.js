import * as types from "../actionTypes";

const paginationInitialState = {
  teamsPageNumber: 0,
  projectsPageNumber: 0,
  clustersPageNumber: 0,
  serversPageNumber: 0,
  servicesGroupsPageNumber: 0,
  servicesPageNumber: 0
};

export function pagination(state = paginationInitialState, action) {
  switch (action.type) {
    case types.SET_BILLING_PROJECTS_FILTER_PAGE_NUMBER:
      return { ...state, serversPageNumber: action.pageNumber };
    case types.SET_BILLING_TEAMS_FILTER_PAGE_NUMBER:
      return { ...state, serversPageNumber: action.pageNumber };
    case types.SET_BILLING_SERVERS_FILTER_PAGE_NUMBER:
      return { ...state, serversPageNumber: action.pageNumber };
    case types.SET_BILLING_SERVICES_GROUPS_FILTER_PAGE_NUMBER:
      return { ...state, servicesGroupsPageNumber: action.pageNumber };
    case types.SET_BILLING_SERVICES_FILTER_PAGE_NUMBER:
      return { ...state, servicesPageNumber: action.pageNumber };
    case types.SET_BILLING_CLUSTERS_FILTER_PAGE_NUMBER:
      return { ...state, clustersPageNumber: action.pageNumber };
    default:
      return state;
  }
}
