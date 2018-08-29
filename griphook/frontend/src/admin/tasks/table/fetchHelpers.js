import * as urls from "./urls";

export const fetchServicesgroupsProjectsTeams = () => {
  const url = urls.SERVICESGROUPS_PROJECTS_TEAMS_GET_ALL;
  const data = {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    }
  };
  return fetch(url, data);
};

export const attachProject = (projectId, servicesgroupId) => {
  const url = urls.PROJECT_ATTACH_TO_SERVICESGROUP;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      project_id: projectId,
      services_group_id: servicesgroupId
    })
  };
  return fetch(url, data);
};

export const attachTeam = (teamId, servicesgroupId) => {
  const url = urls.TEAM_ATTACH_TO_SERVICESGROUP;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access_token")}`
    },
    body: JSON.stringify({
      team_id: teamId,
      services_group_id: servicesgroupId
    })
  };
  return fetch(url, data);
};
