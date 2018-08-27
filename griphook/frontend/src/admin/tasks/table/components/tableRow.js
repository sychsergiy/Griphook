import React, { Component } from "react";

import DropDownBoxComponent from "./dropDown/dropDownBox";

class TableRowComponent extends Component {
  render() {
    return (
      <tr>
        <td>{this.props.servicesGroupTitle}</td>
        <td className=" ">
          <DropDownBoxComponent
            objectsDropDownBox={this.props.projects}
            servicesGroupObjectId={this.props.servicesGroupProjectId}
            servicesGroupId={this.props.servicesGroupId}
            attachObjectToServicesGroup={
              this.props.attachProjectToServicesGroup
            }
          />
        </td>
        <td className=" ">
          <DropDownBoxComponent
            objectsDropDownBox={this.props.teams}
            servicesGroupObjectId={this.props.servicesGroupTeamId}
            servicesGroupId={this.props.servicesGroupId}
            attachObjectToServicesGroup={this.props.attachTeamToServicesGroup}
          />
        </td>
      </tr>
    );
  }
}

export default TableRowComponent;
