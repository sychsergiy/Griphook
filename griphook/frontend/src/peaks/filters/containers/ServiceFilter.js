import React from "react";
import { connect } from "react-redux";

import { getFilteredServices } from "../servicesHelper";

import { selectPeaksTarget } from "../../options/actions";

import { peaksTargetTypes } from "../../../common/constants";

import FilterContainer from "./FilterContainer";

const mapStateToProps = state => ({
  allItems: state.peaks.filters.hierarchy.services,
  visibleItems: getFilteredServices(
    state.peaks.filters.selections,
    state.peaks.filters.hierarchy.services
  ),
  selectedItems: [],
  hideCheckbox: true,
  selectedTargetID: state.peaks.chartsOptions.targetID,
  selectedTargetType: state.peaks.chartsOptions.targetType,
  currentTargetType: peaksTargetTypes.service,
  blockTitle: "Services",
  blockTitleIconClass: "fas fa-cogs"
});

const mapDispatchToProps = dispatch => ({
  selectTarget: targetID => {
    dispatch(selectPeaksTarget(targetID, peaksTargetTypes.service));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(FilterContainer);
