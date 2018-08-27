import React, { Component } from "react";

export const TablePaginationComponent = props => {
  return (
    <div className="row">
      <div className="pagination mx-auto my-2">
        {props.page.previousPageExists ? (
          <button
            className="btn btn btn-outline-primary btn-sm"
            onClick={props.decrementPageNumber}
          >
            Prev
          </button>
        ) : null}
        <span className="page-number px-4">{props.pageNumber}</span>
        {props.page.nextPageExists ? (
          <button
            className="btn btn btn-outline-primary btn-sm"
            onClick={props.incrementPageNumber}
          >
            Next
          </button>
        ) : null}
      </div>
    </div>
  );
};
