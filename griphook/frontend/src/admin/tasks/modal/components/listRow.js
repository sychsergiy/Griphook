import React, { Component } from "react";

export const ListRowComponent = props => {
  return (
    <li className="list-group-item">
      {props.title}
      <i
        className="far fa-trash-alt float-right text-danger"
        onClick={() => props.onRowDelete(props.id)}
      />
    </li>
  );
};
