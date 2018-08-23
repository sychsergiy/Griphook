import React, { Component } from "react";

export const SearchInputComponent = props => {
  return (
    <input
      className="form-control search-input"
      onChange={props.onSearchInputChange}
      type="text"
      placeholder="search..."
    />
  );
};
