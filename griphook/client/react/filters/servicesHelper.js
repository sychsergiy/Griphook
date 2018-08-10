import { isEmpty } from "./common";

export function getFilteredServices(selections, services) {
  let filteredServices = servicesFilter(services)
    .filterByClusters(selections.clusters)
    .filterByServers(selections.servers)
    .filterByServicesGroups(selections.servicesGroups)
    .getItems();
  return filteredServices;
}

function servicesFilter(initialServices) {
  let currentServices = initialServices;

  function filterByClusters(selectedClusters) {
    if (!isEmpty(selectedClusters)) {
      currentServices = currentServices.filter(service =>
        selectedClusters.includes("" + service.cluster_id)
      );
    }
    return this;
  }

  function filterByServers(selectedServers) {
    if (!isEmpty(selectedServers)) {
      currentServices = currentServices.filter(service =>
        selectedServers.includes("" + service.server_id)
      );
    }
    return this;
  }

  function filterByServicesGroups(selectedServicesGroups) {
    if (!isEmpty(selectedServicesGroups)) {
      currentServices = currentServices.filter(service =>
        selectedServicesGroups.includes("" + service.group_id)
      );
    }
    return this;
  }

  return {
    filterByClusters,
    filterByServers,
    filterByServicesGroups,
    getItems: () => currentServices
  };
}
