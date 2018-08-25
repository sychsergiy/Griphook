import React, { Component } from "react";
import { connect } from "react-redux";

import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => ({
  allItems: state.billing.filters.hierarchy.clusters, // for search
  visibleItems: state.billing.filters.hierarchy.clusters, // paginator
  currentTargetType: billingTargetTypes.cluster,
  selectedTargetType: state.billing.options.targetType,
  selectedTargetIDs: state.billing.options.targetIDs,
  blockTitle: "Clusters"
});

const mapDispatchToProps = dispatch => ({
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.cluster));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
