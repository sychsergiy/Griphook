import React, { Component } from "react";
import { connect } from "react-redux";

import { setProjectsFilterPageNumber } from "../actions/pagination";
import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => ({
  allItems: state.billing.filters.hierarchy.projects,
  visibleItems: state.billing.filters.hierarchy.projects,
  pageNumber: state.billing.filters.pagination.projectsPageNumber,
  currentTargetType: billingTargetTypes.project,
  selectedTargetType: state.billing.options.targetType,
  selectedTargetIDs: state.billing.options.targetIDs,
  blockTitle: "Projects"
});

const mapDispatchToProps = dispatch => ({
  setPageNumber: pageNumber => {
    dispatch(setProjectsFilterPageNumber(pageNumber));
  },
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.project));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
