"use strict";

const UPDATE_PROJECT_LIST_URL = "/settings/project";
const MESSAGE_ENTER_PROJECT_TITLE = "Enter project name";


function showAlertMessage(messageText) {
    let message = document.querySelector(".alert");

    if (message !== null) {
        message.querySelector("strong").textContent = messageText;
    }
    else {
        let container = document.getElementById("teams"),
            newAlertMessage;

        newAlertMessage = document.createElement("div");
        newAlertMessage.setAttribute("class", "alert alert-danger alert-dismissible");
        newAlertMessage.innerHTML = `<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                                     <strong>${messageText}</strong>`;
        container.insertBefore(newAlertMessage, container.children[2])
    }
}


function createProject(projectTitle) {
    return fetch(
        UPDATE_PROJECT_LIST_URL,
    {
        method: "POST",
        body: JSON.stringify({
            title: projectTitle
        })
    })
}


function deleteProject(projectId) {
    return fetch(
        UPDATE_PROJECT_LIST_URL,
    {
        method: "DELETE",
        body: JSON.stringify({
            id: projectId
        })
    })
}


function addRowToTable(projectTitle, projectId) {
    let table = document.getElementById("table_body"),
        newRow;

    newRow = document.createElement("tr");
    newRow.setAttribute("data-project-id", projectId);
    newRow.innerHTML = `<td>${projectTitle}</td>
                        <td><button type="button" class="btn btn-sm btn-block btn-danger table-button" data-action="edit_project"><span class="fa fa-pencil-square-o"></span> Edit</button></td>
                        <td><button type="button" class="btn btn-sm btn-block btn-danger table-button" data-action="del_project"><span class="fa fa-trash-o"></span> Delete</button></td>`
    table.insertBefore(newRow, table.children[0])
}


function deleteRowFromTable(target_tr) {
    let table = document.getElementById("table_body");

    table.removeChild(target_tr);
}


function completeProjectList() {
    let projectTitle = document.getElementById("input_project").value;

    if (projectTitle === "") {
        showAlertMessage(MESSAGE_ENTER_PROJECT_TITLE);
    }
    else {
        createProject(projectTitle)
            .then((response) => {
                if (response.status === 200) {
                    response.json()
                        .then(project => {
                            addRowToTable(project.title, project.id);
                        })
                }
                else {
                    response.text()
                        .then((text) => {
                            showAlertMessage(text);
                        });
                }
            })
    }
}


function truncateProjectList(target) {
    let target_tr = target.closest("tr");
    let id = target_tr.getAttribute("data-project-id");

    deleteProject(id)
        .then((response) => {
            if (response.status === 200) {
                deleteRowFromTable(target_tr);
            }
            else {
                response.text()
                    .then((text) => {
                        showAlertMessage(text)
                    });
            }
    });

}


function handlingClickEvent(event) {
    let target = event.target;

    if (target.tagName === "BUTTON") {

        target.add_project = completeProjectList;
        target.del_project = truncateProjectList;

        let action = target.getAttribute("data-action");

        if (action) {
            target[action](target);
        }
    }
}


function ready() {
    document.getElementById("tabs_content").addEventListener("click", handlingClickEvent);
}

document.addEventListener("DOMContentLoaded", ready);
