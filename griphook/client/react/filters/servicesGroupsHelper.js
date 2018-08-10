import { isEmpty } from "./common";

export function getFilteredServicesGroups(selections, ServicesGroups) {
  let filteredServicesGroups = servicesGroupFilter(ServicesGroups)
    .filterByClusters(selections.clusters)
    .filterByServers(selections.servers)
    .getItems();
  return filteredServicesGroups;
}

function servicesGroupFilter(initialServicesGroups) {
  let currentServicesGroups = initialServicesGroups;

  function filterByClusters(selectedClusters) {
    if (!isEmpty(selectedClusters)) {
      currentServicesGroups = currentServicesGroups.filter(servicesGroup =>
        isServicesGroupInCluster(servicesGroup, selectedClusters)
      );
    }
    return this;
  }

  function filterByServers(selectedServers) {
    if (!isEmpty(selectedServers)) {
      currentServicesGroups = currentServicesGroups.filter(servicesGroup =>
        isServicesGroupInServer(servicesGroup, selectedServers)
      );
    }
    return this;
  }

  return {
    filterByServers,
    filterByClusters,
    getItems: () => currentServicesGroups
  };
}

function isServicesGroupInCluster(servicesGroup, selectedClusters) {
  for (let clusterID of servicesGroup.clusters_ids) {
    if (selectedClusters.includes("" + clusterID)) {
      return true;
    }
  }
}

function isServicesGroupInServer(servicesGroup, selectedClusters) {
  for (let serverID of servicesGroup.servers_ids) {
    if (selectedClusters.includes("" + serverID)) {
      return true;
    }
  }
}
