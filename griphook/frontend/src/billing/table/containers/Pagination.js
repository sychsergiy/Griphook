import React, { Component } from "react";

import { connect } from "react-redux";

import { setBillingTablePageNumber } from "../actions/groups";

const BillingTablePaginationComponent = props => {
  const buttonClass = "btn btn-outline-primary btn-sm";
  const disabledButtonClass = "btn btn-outline-primary btn-sm disabled";

  const isPreviousPageButtonActive = props.previousPageExists && !props.loading;
  const isNextPageButtonActive = props.nextPageExists && !props.loading;

  return (
    <div className="row">
      <div className="pagination mx-auto mt-4">
        <button
          className={
            isPreviousPageButtonActive ? buttonClass : disabledButtonClass
          }
          onClick={
            isPreviousPageButtonActive
              ? () => props.setPageNumber(props.pageNumber - 1)
              : null
          }
        >
          Prev
        </button>
        <span className="page-number pl-4 pr-2">{props.pageNumber}</span>
        ...
        <span className="max-page-number pl-2 pr-4">{props.pagesCount}</span>
        <button
          className={isNextPageButtonActive ? buttonClass : disabledButtonClass}
          onClick={
            isNextPageButtonActive
              ? () => props.setPageNumber(props.pageNumber + 1)
              : null
          }
        >
          Next
        </button>
      </div>
    </div>
  );
};

const mapStateToProps = state => ({
  loading: state.billing.table.groups.loading,
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
