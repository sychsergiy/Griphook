import React, { Component } from "react";

import TableRowComponent from "./tableRow";

class TableBodyComponent extends Component {
  renderTableRows(dataAfterPagination) {
    return dataAfterPagination.map(servicesGroup => {
      if (servicesGroup.project_id == null) {
        servicesGroup.project_id = "null";
      } else if (servicesGroup.team_id == null) {
        servicesGroup.team_id = "null";
      }
      return (
        <TableRowComponent
          key={servicesGroup.id}
          servicesGroupId={servicesGroup.id}
          servicesGroupTitle={servicesGroup.title}
          servicesGroupProjectId={servicesGroup.project_id}
          servicesGroupTeamId={servicesGroup.team_id}
          projects={this.props.projects}
          teams={this.props.teams}
          attachProjectToServicesGroup={this.props.attachProjectToServicesGroup}
          attachTeamToServicesGroup={this.props.attachTeamToServicesGroup}
        />
      );
    });
  }

  render() {
    return (
      <tbody>{this.renderTableRows(this.props.dataAfterPagination)}</tbody>
    );
  }
}

export default TableBodyComponent;
