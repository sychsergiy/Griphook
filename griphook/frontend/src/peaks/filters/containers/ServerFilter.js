import React from "react";
import { connect } from "react-redux";

import { selectPeaksTarget } from "../../options/actions";

import { separateSelectedItems } from "../../../common/filtersHelper/common";
import { getFilteredServers } from "../../../common/filtersHelper/servers";

import {
  selectServerFilter,
  unSelectServerFilter
} from "../actions/selections";

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
  unSelectFilterItem: serverID => {
    dispatch(unSelectServerFilter(serverID));
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
