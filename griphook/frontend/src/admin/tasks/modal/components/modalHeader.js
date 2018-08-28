import React, { Component } from "react";

import { listDataType } from "../constants";

export const ModalHeaderComponent = props => {
  let modalTitle = "";
  if (props.listDataType === listDataType.projects) {
    modalTitle = "Edit Projects";
  } else if (props.listDataType === listDataType.teams) {
    modalTitle = "Edit Teams";
  }

  return (
    <div className="modal-header">
      <h5 className="modal-title">
        <i className="fas fa-pen-nib mr-2" />
        {modalTitle}
      </h5>
      <button
        type="button"
        className="close"
        data-dismiss="modal"
        aria-label="Close"
        onClick={() => {
          props.hideModal();
        }}
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  );
};
