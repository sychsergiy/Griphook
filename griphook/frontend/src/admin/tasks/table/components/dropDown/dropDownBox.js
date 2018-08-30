import React, { Component } from "react";

import { DropDownElementComponent } from "./dropDownElement";

class DropDownBoxComponent extends Component {
  renderDropDownElement() {
    return this.props.objectsDropDownBox.map(objectDropDownElement => {
      return (
        <DropDownElementComponent
          key={objectDropDownElement.id}
          objectDropDownElementId={objectDropDownElement.id}
          objectDropDownElementTitle={objectDropDownElement.title}
        />
      );
    });
  }

  render() {
    return (
      <select
        className="custom-select"
        value={(this.props.servicesGroupObjectId).toString()}
        onChange={event =>
          this.props.attachObjectToServicesGroup(
            event,
            this.props.servicesGroupId
          )
        }
      >
        <option value="null">Not attached</option>
        {this.renderDropDownElement()}
      </select>
    );
  }
}

export default DropDownBoxComponent;
