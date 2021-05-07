import {listDataType} from "./constants"

import {
  fetchProjects,
  fetchTeams,
  createProject,
  createTeam,
  deleteProject,
  deleteTeam,
  updateProjectTitle,
  updateTeamTitle
} from './fetchHelpers';


export const getObjects = dataType =>  {
  if (dataType === listDataType.projects) {
    return fetchProjects()
  }
  else if (dataType === listDataType.teams) {
    return fetchTeams()
  }
}

export const createObject = (dataType, objectTitle) =>  {
  if (dataType === listDataType.projects) {
      return createProject(objectTitle)
  }
  else if (dataType === listDataType.teams) {
    return createTeam(objectTitle)
  }
}

export const updateObjectTitle = (dataType, objectId, objectTitle) =>  {
  if (dataType === listDataType.projects) {
    return updateProjectTitle(objectId, objectTitle)
  }
  else if (dataType === listDataType.teams) {
    return updateTeamTitle(objectId, objectTitle)
  }
}

export const deleteObject = (dataType, objectId) =>  {
  if (dataType === listDataType.projects) {
    return deleteProject(objectId)
  }
  else if (dataType === listDataType.teams) {
    return deleteTeam(objectId)
  }
}
