import React, { Component } from "react";

export const EditButtonsComponent = props => {
  return (
    <div className="ml-auto">
      <button
        className="btn btn-sm btn-outline-primary"
        onClick={() => {
          props.showModal("projects");
        }}
      >
        <i className="fas fa-project-diagram mr-2" />Edit projects
      </button>
      <button
        className="btn btn-sm btn-outline-primary ml-3"
        onClick={() => {
          props.showModal("teams");
        }}
      >
        <i className="fas fa-people-carry mr-2" />Edit teams
      </button>
    </div>
  );
};
