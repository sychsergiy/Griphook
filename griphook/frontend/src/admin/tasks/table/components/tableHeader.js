import React, { Component } from "react";

class TableHeaderComponent extends Component {
  render() {
    return (
      <thead>
        <tr>
          <th scope="col">Services group</th>
          <th scope="col">Project</th>
          <th scope="col">Team</th>
        </tr>
      </thead>
    );
  }
}

export default TableHeaderComponent;
