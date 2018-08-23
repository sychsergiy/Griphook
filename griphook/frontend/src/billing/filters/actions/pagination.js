import * as types from "../actionTypes";

export const setProjectsFilterPageNumber = pageNumber => ({
  type: types.SET_BILLING_PROJECTS_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setTeamsFilterPageNumber = pageNumber => ({
  type: types.SET_BILLING_TEAMS_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setClustersPageNumber = pageNumber => ({
  type: types.SET_BILLING_CLUSTERS_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setServersFilterPageNumber = pageNumber => ({
  type: types.SET_BILLING_SERVERS_FILTER_PAGE_NUMBER,
  pageNumber
});

export const setServicesGroupsFilterPageNumber = pageNumber => ({
  type: types.SET_BILLING_SERVICES_GROUPS_FILTER_PAGE_NUMBER,
  pageNumber
});
