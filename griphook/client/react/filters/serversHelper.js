import { isEmpty } from "./common";

export function getFilteredServers(selections, allServers) {
  let filteredServers = getServersFilteredByClusters(
    selections.clusters,
    allServers
  );
  return filteredServers;
}

export function getServersFilteredByClusters(selectedClusters, servers) {
  if (isEmpty(selectedClusters)) {
    return servers;
  }

  let filteredServers = servers.filter(server =>
    selectedClusters.includes("" + server.cluster_id)
  );
  return filteredServers;
}
