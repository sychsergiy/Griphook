import React, { Component } from "react";

export const ModalFooterComponent = props => {
  return (
    <div className="modal-footer">
      <button type="button" className="btn btn-secondary" data-dismiss="modal" onClick={() => {props.hideModal();}}>
        Close
      </button>
    </div>
  );
};
