import React from "react";
import { connect } from "react-redux";

import { separateSelectedItems } from "../../../common/filtersHelper/common";
import { getFilteredServicesGroups } from "../../../common/filtersHelper/servicesGroups";

import { selectPeaksTarget } from "../../options/actions";

import {
  selectServicesGroupFilter,
  unSelectServicesGroupFilter
} from "../actions/selections";

import { peaksTargetTypes } from "../../../common/constants";

import FilterContainer from "./FilterContainer";

const mapStateToProps = state => {
  let selections = state.peaks.filters.selections;
  let [selectedGroups, visibleGroups] = separateSelectedItems(
    state.peaks.filters.hierarchy.servicesGroups,
    selections.servicesGroups
  );

  let filteredGroups = getFilteredServicesGroups(selections, visibleGroups);
  return {
    selectedItems: selectedGroups,
    visibleItems: filteredGroups,
    blockTitle: "Services Groups",
    selectedTargetID: state.peaks.chartsOptions.targetID,
    selectedTargetType: state.peaks.chartsOptions.targetType,
    currentTargetType: peaksTargetTypes.servicesGroup,
    blockTitleIconClass: "fas fa-object-group mr-2"
  };
};

const mapDispatchToProps = dispatch => ({
  selectFilterItem: servicesGroupID => {
    dispatch(selectServicesGroupFilter(servicesGroupID));
  },
  unSelectFilterItem: servicesGroupID => {
    dispatch(unSelectServicesGroupFilter(servicesGroupID));
  },

  selectTarget: targetID => {
    dispatch(selectPeaksTarget(targetID, peaksTargetTypes.servicesGroup));
  }
});

const ServicesGroupFilterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(FilterContainer);

export default ServicesGroupFilterContainer;
