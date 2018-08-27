import React, { Component } from "react";

import { ListRowComponent } from "./listRow";

class ListBlockComponent extends Component {
  renderListRows() {
    return this.props.listData.map(object => {
      return (
        <ListRowComponent
          key={object.id}
          title={object.title}
          id={object.id}
          onRowDelete={this.props.onRowDelete}
        />
      );
    });
  }
  render() {
    return (
      <div className="col-12">
        <ul className="list-group list-group-flush">{this.renderListRows()}</ul>
      </div>
    );
  }
}

export default ListBlockComponent;
