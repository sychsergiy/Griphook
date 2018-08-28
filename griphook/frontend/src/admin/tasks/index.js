import React, { Component } from "react";

import TableContainer from "./table";
import ModalComponent from "./modal"

class TasksSettingsPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      show: false,
      modalListDataType: "projects"
    };
    this.showModal = this.showModal.bind(this);
    this.hideModal = this.hideModal.bind(this);
  }

  showModal(listDataType) {
    console.log(listDataType);
    this.setState({ show: true , modalListDataType: listDataType});
  };

  hideModal() {
    this.setState({ show: false });
  };

  render() {
    return(
      <div>
        <h3>Tasks conformity settings</h3>
        <p className="text-muted">Choose team and project for services groups</p>
        <TableContainer showModal={this.showModal}/>
        <ModalComponent show={this.state.show} hideModal={this.hideModal} listDataType={this.state.modalListDataType}/>
      </div>
    );
  }
}

export default TasksSettingsPage;
