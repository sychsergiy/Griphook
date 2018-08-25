import React from "react";
import { connect } from "react-redux";

import { getFilteredServicesGroups } from "../servicesGroupsHelper";

import { selectPeaksTarget } from "../../options/actions";

import {
  selectServicesGroupFilter,
  unSelectServicesGroupFilter
} from "../actions/selections";

import { separateSelectedItems } from "../common";
import { peaksTargetTypes } from "../../../common/constants";

import FilterContainer from "./FilterContainer";

const mapStateToProps = state => {
  let allGroups = state.peaks.filters.hierarchy.servicesGroups;
  let selections = state.peaks.filters.selections;
  let [selectedGroups, visibleGroups] = separateSelectedItems(
    allGroups,
    selections.servicesGroups
  );

  let filteredGroups = getFilteredServicesGroups(selections, visibleGroups);
  return {
    allItems: allGroups,
    selectedItems: selectedGroups,
    visibleItems: filteredGroups,
    blockTitle: "Services Groups",
    selectedTargetID: state.peaks.chartsOptions.targetID,
    selectedTargetType: state.peaks.chartsOptions.targetType,
    currentTargetType: peaksTargetTypes.servicesGroup,
    blockTitleIconClass: "fas fa-object-group"
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
