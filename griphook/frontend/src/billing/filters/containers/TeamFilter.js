import React, { Component } from "react";
import { connect } from "react-redux";

import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import { separateSelectedItems } from "../../../common/filtersHelper/common";

import { selectTeamFilter, unSelectTeamFilter } from "../actions/selections";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => {
  let [selectedTeams, unSelectedTeams] = separateSelectedItems(
    state.billing.filters.hierarchy.teams,
    state.billing.filters.selections.teams
  );
  return {
    selectedItems: selectedTeams,
    visibleItems: unSelectedTeams,
    currentTargetType: billingTargetTypes.team,
    selectedTargetType: state.billing.options.targetType,
    selectedTargetIDs: state.billing.options.targetIDs,
    blockTitle: "Teams",
    blockTitleIconClass: "fas fa-people-carry mr-2",
    loading: state.billing.filters.hierarchy.loading,
    error: state.billing.filters.hierarchy.error
  };
};

const mapDispatchToProps = dispatch => ({
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.team));
  },
  selectFilterItem: projectID => {
    dispatch(selectTeamFilter(projectID));
  },
  unSelectFilterItem: projectID => {
    dispatch(unSelectTeamFilter(projectID));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
