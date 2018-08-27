import React, { Component } from "react";

export const SearchInputComponent = props => {
  return (
    <div className="input-group input-group-sm col-12 col-sm-8 col-md-7 col-lg-5">
      <input
        type="text"
        className="form-control"
        onChange={props.onSearchInputChange}
        placeholder="Search..."
        aria-label="Search..."
        aria-describedby="ba sic-addon1"
      />
      <div className="input-group-append">
        <span className="input-group-text text-primary" id="basic-addon1">
          <i className="fas fa-search" />
        </span>
      </div>
    </div>
  );
};
