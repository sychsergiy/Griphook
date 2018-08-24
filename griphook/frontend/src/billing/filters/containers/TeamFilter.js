import React, { Component } from "react";
import { connect } from "react-redux";

import { setTeamsFilterPageNumber } from "../actions/pagination";
import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => ({
  allItems: state.billing.filters.hierarchy.teams,
  visibleItems: state.billing.filters.hierarchy.teams,
  pageNumber: state.billing.filters.pagination.teamsPageNumber,
  currentTargetType: billingTargetTypes.team,
  selectedTargetType: state.billing.options.targetType,
  selectedTargetIDs: state.billing.options.targetIDs,
  blockTitle: "Teams"
});

const mapDispatchToProps = dispatch => ({
  setPagetNumber: pageNumber => {
    dispatch(setTeamsFilterPageNumber(pageNumber));
  },
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.team));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
