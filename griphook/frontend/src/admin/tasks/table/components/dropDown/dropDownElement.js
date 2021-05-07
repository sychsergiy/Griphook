import React, { Component } from "react";

export const DropDownElementComponent = props => {
  return (
    <option value={props.objectDropDownElementId}>
      {props.objectDropDownElementTitle}
    </option>
  );
};
