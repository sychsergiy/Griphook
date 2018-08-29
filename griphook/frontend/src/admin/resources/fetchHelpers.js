import * as urls from "./urls";


export const fetchServers = () => {
  const url = urls.SERVERS_GET_ALL;
  const data = {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
  };
  return fetch(url, data);
};


export const updateServerCPUPrice = (serverId, serverCPUPrice) =>  {
  const url = urls.SERVERS_UPDATE_CPU_PRICE;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({id: serverId, cpu_price: serverCPUPrice})
  };
  return fetch(url, data)
};


export const updateServerMemoryPrice = (serverId, serverMemoryPrice) =>  {
  const url = urls.SERVERS_UPDATE_MEMORY_PRICE;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({id: serverId, memory_price: serverMemoryPrice})
  };
  return fetch(url, data)
};


export const fetchClusters = () => {
  const url = urls.CLUSTERS_GET_ALL;
  const data = {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
  };
  return fetch(url, data);
};


export const updateClusterCPUPrice = (clusterId, clusterCPUPrice) =>  {
  const url = urls.CLUSTERS_UPDATE_CPU_PRICE;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({id: clusterId, cpu_price: clusterCPUPrice})
  };
  return fetch(url, data)
};


export const updateClusterMemoryPrice = (clusterId, clusterMemoryPrice) =>  {
  const url = urls.CLUSTERS_UPDATE_MEMORY_PRICE;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({id: clusterId, memory_price: clusterMemoryPrice})
  };
  return fetch(url, data)
};
