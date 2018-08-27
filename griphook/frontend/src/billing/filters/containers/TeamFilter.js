import React, { Component } from "react";
import { connect } from "react-redux";

import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => ({
  allItems: state.billing.filters.hierarchy.teams,
  visibleItems: state.billing.filters.hierarchy.teams,
  currentTargetType: billingTargetTypes.team,
  selectedTargetType: state.billing.options.targetType,
  selectedTargetIDs: state.billing.options.targetIDs,
  blockTitle: "Teams"
});

const mapDispatchToProps = dispatch => ({
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.team));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
