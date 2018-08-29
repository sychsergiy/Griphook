import React, { Component } from "react";
import ReactDOM from "react-dom";

import {ModalHeaderComponent} from "./components/modalHeader"
import {ModalFooterComponent} from "./components/modalFooter"

import ModalBodyContainer from "./containers/ModalBody"


export const ModalComponent = props => {
  const modalClassName = props.show ? "modal fade d-block show" : "modal fade d-none";
  const backdropClassName = props.show ? "modal-backdrop fade show" : "modal-backdrop fade d-none";
  return (
    <div>
      <div className={modalClassName} tabIndex="-1" role="dialog">
        <div className="modal-dialog modal-dialog-centered modal-lg" role="document">
          <div className="modal-content">
            <ModalHeaderComponent hideModal={props.hideModal} listDataType={props.listDataType}/>
            <ModalBodyContainer listDataType={props.listDataType}/>
            <ModalFooterComponent hideModal={props.hideModal}/>
          </div>
        </div>
      </div>
      <div className={backdropClassName}></div>
    </div>
  );
};

export default ModalComponent;
