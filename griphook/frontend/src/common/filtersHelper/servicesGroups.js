import { isEmpty } from "./common";

export function getFilteredServicesGroups(selections, ServicesGroups) {
  // TODO: this function must take cluster and servers as arugments
  let filteredServicesGroups = servicesGroupFilter(ServicesGroups)
    .filterByClusters(selections.clusters)
    .filterByServers(selections.servers)
    .getItems();
  return filteredServicesGroups;
}

export function servicesGroupFilter(initialServicesGroups) {
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

  function filterByProjects(selectedProjects) {
    if (!isEmpty(selectedProjects)) {
      currentServicesGroups = currentServicesGroups.filter(servicesGroup =>
        isServicesGroupInProject(servicesGroup, selectedProjects)
      );
    }
    return this;
  }

  function filterByTeams(selectedTeams) {
    if (!isEmpty(selectedTeams)) {
      currentServicesGroups = currentServicesGroups.filter(servicesGroup =>
        isServicesGroupInTeam(servicesGroup, selectedTeams)
      );
    }
    return this;
  }

  return {
    filterByServers,
    filterByClusters,
    filterByProjects,
    filterByTeams,
    getItems: () => currentServicesGroups
  };
}

function isServicesGroupInCluster(servicesGroup, selectedClusters) {
  for (let clusterID of servicesGroup.clusters_ids) {
    if (selectedClusters.includes(clusterID)) {
      return true;
    }
  }
}

function isServicesGroupInServer(servicesGroup, selectedClusters) {
  for (let serverID of servicesGroup.servers_ids) {
    if (selectedClusters.includes(serverID)) {
      return true;
    }
  }
}

function isServicesGroupInProject(servicesGroup, selectedProjects) {
  for (let groupID of servicesGroup.projects_ids) {
    if (selectedProjects.includes(groupID)) {
      return true;
    }
  }
}

function isServicesGroupInTeam(servicesGroup, selectedTeams) {
  for (let groupID of servicesGroup.teams_ids) {
    if (selectedTeams.includes(groupID)) {
      return true;
    }
  }
}
