import * as urls from './urls';


export const fetchProjects = () =>  {
  const url = urls.PROJECT_GET_ALL;
  const data = {
    method: "GET"
  };
  return fetch(url, data)
};

export const fetchTeams = () =>  {
  const url = urls.TEAM_GET_ALL;
  const data = {
    method: "GET"
  };
  return fetch(url, data)
};

export const createProject = projectTitle =>  {
  const url = urls.PROJECT_CREATE;
  const data = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({title: projectTitle})
  };
  return fetch(url, data)
};

export const createTeam = teamTitle =>  {
  const url = urls.TEAM_CREATE;
  const data = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({title: teamTitle})
  };
  return fetch(url, data)
};

export const updateProjectTitle = (projectId, projectTitle) =>  {
  const url = urls.PROJECT_UPDATE_TITLE;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({id: projectId, title: projectTitle})
  };
  return fetch(url, data)
};


export const updateTeamTitle = (teamId, teamTitle) =>  {
  const url = urls.TEAM_UPDATE_TITLE;
  const data = {
    method: "PUT",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({id: teamId, title: teamTitle})
  };
  return fetch(url, data)
};

export const deleteProject = projectId =>  {
  const url = urls.PROJECT_DELETE;
  const data = {
    method: "DELETE",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({id: projectId})
  };
  return fetch(url, data)
};

export const deleteTeam = teamId =>  {
  const url = urls.TEAM_DELETE;
  const data = {
    method: "DELETE",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({id: teamId})
  };
  return fetch(url, data)
};
