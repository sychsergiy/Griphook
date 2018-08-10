import * as types from "../actionTypes";

export const setServersFilterPageNumber = pageNumber => ({
  type: types.SET_SERVERS_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setServicesGroupsFilterPageNumber = pageNumber => ({
  type: types.SET_SERVICES_GROUPS_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setServicesFilterPageNumber = pageNumber => ({
  type: types.SET_SERVICES_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setClustersPageNumber = pageNumber => ({
  type: types.SET_CLUSTERS_FILTER_PAGE_NUMBER,
  pageNumber
});
