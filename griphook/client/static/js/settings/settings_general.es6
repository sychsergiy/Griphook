"use strict";

const TEAM_SETTINGS_API_URL = "/settings/team";
const PROJECT_SETTINGS_API_URL = "/settings/project";
const MESSAGE_EMPTY_INPUT = "Enter name";


function showAlertMessage(messageText, containerId) {
    let message = document.querySelector(".alert");

    if (message !== null) {
        message.querySelector("strong").textContent = messageText;
    }
    else {
        let container = document.getElementById(containerId),
            newAlertMessage;

        newAlertMessage = document.createElement("div");
        newAlertMessage.setAttribute("class", "alert alert-danger alert-dismissible");
        newAlertMessage.innerHTML = `<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                     <strong>${messageText}</strong>`;
        container.insertBefore(newAlertMessage, container.children[2])
    }
}

function createElement(settingsURL, elementTitle) {
    return fetch(
        settingsURL,
    {
        method: "POST",
        body: JSON.stringify({
            title: elementTitle
        })
    })
}

function updateElement(settingsURL, elementId, elementNewTitle) {
    return fetch(
        settingsURL,
    {
        method: "PUT",
        body: JSON.stringify({
            id: elementId,
            title: elementNewTitle
        })
    })
}

function deleteElement(settingsURL, elementId) {
    return fetch(
        settingsURL,
    {
        method: "DELETE",
        body: JSON.stringify({
            id: elementId
        })
    })
}

function addRowToTable(elementTitle, elementId, tableId, dataActionEdit, dataActionDelete, nameAtributeId) {
    let table = document.getElementById(tableId),
        newRow;

    newRow = document.createElement("tr");
    newRow.setAttribute(nameAtributeId, elementId);
    newRow.innerHTML = `<td>${elementTitle}</td>
                        <td><button type="button" class="btn btn-sm btn-block btn-danger table-button" data-action=${dataActionEdit}><span class="fa fa-pencil-square-o"></span> Edit</button></td>
                        <td><button type="button" class="btn btn-sm btn-block btn-danger table-button" data-action=${dataActionDelete}><span class="fa fa-trash-o"></span> Delete</button></td>`;
    table.insertBefore(newRow, table.children[0]);
}

function deleteRowFromTable(tableId, targetTR) {
    let table = document.getElementById(tableId);

    table.removeChild(targetTR);
}

function editModeOn(editedItem, editButton) {
    editedItem.setAttribute("contenteditable", "true");
    editedItem.setAttribute("style", "background: lightgreen");
    editButton.innerHTML = '<span class="fa fa-check-square-o"></span> Save';
}

function editModeOff(editedItem, editButton) {
    editedItem.removeAttribute("contenteditable");
    editedItem.removeAttribute("style");
    editButton.innerHTML = '<span class="fa fa-pencil-square-o"></span> Edit';
}

function addNewTeam() {
    const dataActionEdit = "edit_team";
    const dataActionDelete = "del_team";
    const tableId  = "table-body-teams";
    const nameAtributeId = "data-team-id";
    const containerId = "teams";

    let teamTitle = document.getElementById("input_team").value;

    if (teamTitle === "") {
        showAlertMessage(MESSAGE_EMPTY_INPUT, containerId);
    }
    else {
        createElement(TEAM_SETTINGS_API_URL, teamTitle)
            .then((response) => {
                if (response.status === 200) {
                    response.json()
                        .then(team => {
                            addRowToTable(team.title, team.id, tableId, dataActionEdit, dataActionDelete, nameAtributeId);
                        })
                }
                else {
                    response.json()
                        .then(data => {
                           showAlertMessage(data.error, containerId);
                        })
                }
            })
    }
}

function addNewProject() {
    const dataActionEdit = "edit_project";
    const dataActionDelete = "del_project";
    const tableId  = "table-body-projects";
    const nameAtributeId = "data-project-id";
    const containerId = "projects";

    let projectTitle = document.getElementById("input_project").value;

    if (projectTitle === "") {
        showAlertMessage(MESSAGE_EMPTY_INPUT, containerId);
    }
    else {
        createElement(PROJECT_SETTINGS_API_URL, projectTitle)
            .then((response) => {
                if (response.status === 200) {
                    response.json()
                        .then(project => {
                            addRowToTable(project.title, project.id, tableId, dataActionEdit, dataActionDelete, nameAtributeId);
                        })
                }
                else {
                    response.json()
                        .then(data => {
                           showAlertMessage(data.error, containerId);
                        })
                }
            })
    }
}

function deleteTeam(target) {
    const tableId  = "table-body-teams";
    const containerId = "teams";

    let targetTR = target.closest("tr");
    let elementId = targetTR.getAttribute("data-team-id");

    deleteElement(TEAM_SETTINGS_API_URL, elementId)
        .then((response) => {
            if (response.status === 200) {
                deleteRowFromTable(tableId, targetTR);
            }
            else {
                response.json()
                    .then(data => {
                       showAlertMessage(data.error, containerId);
                    })
            }
    });
}

function deleteProject(target) {
    const tableId  = "table-body-projects";
    const containerId = "projects";

    let targetTR = target.closest("tr");
    let elementId = targetTR.getAttribute("data-project-id");

    deleteElement(PROJECT_SETTINGS_API_URL, elementId)
        .then((response) => {
            if (response.status === 200) {
                deleteRowFromTable(tableId, targetTR);
            }
            else {
                response.json()
                    .then(data => {
                       showAlertMessage(data.error, containerId);
                    })
            }
    });
}

function editProjectTitle(editButton) {
    const containerId = "projects";
    let editedItem = editButton.closest("tr").firstElementChild;

    if (editedItem.getAttribute("contenteditable") === "true") {
        let elementId = editButton.closest("tr").getAttribute("data-project-id");
        let elementNewTitle = editedItem.textContent;

        updateElement(PROJECT_SETTINGS_API_URL, elementId, elementNewTitle)
            .then((response) => {
                if (response.status !== 200) {
                    response.json()
                        .then(data => {
                           showAlertMessage(data.error, containerId);
                        });
                }
                editModeOff(editedItem, editButton);
            });
    }
    else {
        editModeOn(editedItem, editButton);
    }
}

function editTeamTitle(editButton) {
    const containerId = "teams";
    let editedItem = editButton.closest("tr").firstElementChild;

    if (editedItem.getAttribute("contenteditable") === "true") {
        let elementId = editButton.closest("tr").getAttribute("data-team-id");
        let elementNewTitle = editedItem.textContent;

        updateElement(TEAM_SETTINGS_API_URL, elementId, elementNewTitle)
            .then((response) => {
                if (response.status !== 200) {
                    response.json()
                        .then(data => {
                           showAlertMessage(data.error, containerId);
                        });
                }
                editModeOff(editedItem, editButton);
            });
    }
    else {
        editModeOn(editedItem, editButton);
    }
}

function handlingClickEvent(event) {
    let target = event.target;

    if (target.tagName === "BUTTON") {
        target.add_project = addNewProject;
        target.del_project = deleteProject;

        target.add_team = addNewTeam;
        target.del_team = deleteTeam;

        target.edit_project = editProjectTitle;
        target.edit_team = editTeamTitle;

        let action = target.getAttribute("data-action");

        if (action) {
            target[action](target);
        }
    }
}

function handleKeydownEvent(event) {
    if (event.keyCode === 13) {
        let editedItem = event.target;

        if (editedItem.hasAttribute("contenteditable")) {
            editModeOff(editedItem, editedItem.nextElementSibling.firstElementChild);
        }
    }
}

function ready() {
    document.getElementById("tabs_content").addEventListener("click", handlingClickEvent);
    document.getElementById("table-body-projects").addEventListener("keydown", handleKeydownEvent);
    document.getElementById("table-body-teams").addEventListener("keydown", handleKeydownEvent);
}

document.addEventListener("DOMContentLoaded", ready);
