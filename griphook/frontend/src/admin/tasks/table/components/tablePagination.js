import React, { Component } from "react";

export const TablePaginationComponent = props => {
  return (
    <div className="row">
      <div className="pagination mx-auto my-2">
        <button
          className="btn btn btn-outline-primary btn-sm"
          disabled={!props.page.previousPageExists}
          onClick={props.decrementPageNumber}
        >
          Prev
        </button>
        <span className="page-number px-4">{props.pageNumber}</span>
        <span>. . .</span>
        <span className="page-number px-4">{props.page.amountAllPages}</span>

        <button
          className="btn btn btn-outline-primary btn-sm"
          disabled={!props.page.nextPageExists}
          onClick={props.incrementPageNumber}
        >
          Next
        </button>
      </div>
    </div>
  );
};
