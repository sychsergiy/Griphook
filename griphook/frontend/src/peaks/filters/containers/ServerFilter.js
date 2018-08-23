import React, { Component } from "react";
import { connect } from "react-redux";

import { selectPeaksTarget } from "../../options/actions";

import { getFilteredServers } from "../serversHelper";

import {
  selectServerFilter,
  unselectServerFilter
} from "../actions/selections";

import { separateSelectedItems } from "../common";
import { peaksTargetTypes } from "../../../common/constants";

import FilterContainer from "./FilterContainer";

const mapStateToProps = state => {
  let allServers = state.peaks.filters.hierarchy.servers;
  let selections = state.peaks.filters.selections;
  let [selectedServers, visibleServers] = separateSelectedItems(
    allServers,
    selections.servers
  );
  let filteredServers = getFilteredServers(selections, visibleServers);
  return {
    allItems: allServers,
    selectedItems: selectedServers,
    visibleItems: filteredServers,
    blockTitle: "Servers",
    selectedTargetID: state.peaks.chartsOptions.targetID,
    selectedTargetType: state.peaks.chartsOptions.targetType,
    currentTargetType: peaksTargetTypes.server,
    blockTitleIconClass: "fas fa-server mr-2"
  };
};
const mapDispatchToProps = dispatch => ({
  selectFilterItem: serverID => {
    dispatch(selectServerFilter(serverID));
  },
  unselectFilterItem: serverID => {
    dispatch(unselectServerFilter(serverID));
  },
  selectTarget: targetID => {
    dispatch(selectPeaksTarget(targetID, peaksTargetTypes.server));
  }
});

const ServerFilterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(FilterContainer);

export default ServerFilterContainer;
