import React, { Component } from "react";

import { connect } from "react-redux";

import { setBillingTablePageNumber } from "../actions/groups";

const BillingTablePaginationComponent = props => {
  const buttonClass = "btn btn-outline-primary btn-sm";
  const disabledButtonClass = "btn btn-outline-primary btn-sm disabled";

  return (
    <div className="row">
      <div className="pagination mx-auto mt-4">
        <button
          className={props.previousPageExists ? buttonClass : disabledButtonClass}
          onClick={() => props.setPageNumber(props.pageNumber - 1)}
        >
          Prev
        </button>
        <span className="page-number pl-4 pr-2">{props.pageNumber}</span>
        ...
        <span className="max-page-number pl-2 pr-4">{props.pagesCount}</span>
        <button
          className={props.nextPageExists ? buttonClass : disabledButtonClass}
          onClick={() => props.setPageNumber(props.pageNumber + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

const mapStateToProps = state => ({
  pageNumber: state.billing.table.groups.pageNumber,
  pagesCount: state.billing.table.groups.pagesCount,
  nextPageExists: state.billing.table.groups.nextPageExists,
  previousPageExists: state.billing.table.groups.previousPageExists
});
const mapDispatchToProps = dispatch => ({
  setPageNumber: pageNumber => {
    dispatch(setBillingTablePageNumber(pageNumber));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BillingTablePaginationComponent);
