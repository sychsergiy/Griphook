import React, { Component } from "react";
import { connect } from "react-redux";

import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => ({
  allItems: state.billing.filters.hierarchy.servers,
  visibleItems: state.billing.filters.hierarchy.servers,
  currentTargetType: billingTargetTypes.server,
  selectedTargetType: state.billing.options.targetType,
  selectedTargetIDs: state.billing.options.targetIDs,
  blockTitle: "Servers"
});

const mapDispatchToProps = dispatch => ({
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.server));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
