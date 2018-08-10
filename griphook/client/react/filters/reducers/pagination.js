import * as types from "../actionTypes";

const paginationInitialState = {
  clustersPageNumber: 0,
  serversPageNumber: 0,
  servicesGroupsPageNumber: 0,
  servicesPageNumber: 0
};

export function pagination(state = paginationInitialState, action) {
  switch (action.type) {
    case types.SET_SERVERS_FILTER_PAGE_NUMBER:
      return { ...state, serversPageNumber: action.pageNumber };
    case types.SET_SERVICES_GROUPS_FILTER_PAGE_NUMBER:
      return { ...state, servicesGroupsPageNumber: action.pageNumber };
    case types.SET_SERVICES_FILTER_PAGE_NUMBER:
      return { ...state, servicesPageNumber: action.pageNumber };
    case types.SET_CLUSTERS_FILTER_PAGE_NUMBER:
      return { ...state, clustersPageNumber: action.pageNumber };
    default:
      return state;
  }
}
