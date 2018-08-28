import React from "react";
import { connect } from "react-redux";

import { getFilteredServices } from "../../../common/filtersHelper/services";

import { selectPeaksTarget } from "../../options/actions";

import { peaksTargetTypes } from "../../../common/constants";

import FilterContainer from "./FilterContainer";

const mapStateToProps = state => ({
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
  blockTitleIconClass: "fas fa-cogs mr-2",
  loading: state.peaks.filters.hierarchy.loading,
  error: state.peaks.filters.hierarchy.error
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
