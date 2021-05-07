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
  let selections = state.peaks.filters.selections;
  let [selectedServers, visibleServers] = separateSelectedItems(
    state.peaks.filters.hierarchy.servers,
    selections.servers
  );
  let filteredServers = getFilteredServers(selections, visibleServers);
  return {
    selectedItems: selectedServers,
    blockTitle: "Servers",
    selectedTargetID: state.peaks.chartsOptions.targetID,
    selectedTargetType: state.peaks.chartsOptions.targetType,
    visibleItems: filteredServers,
    currentTargetType: peaksTargetTypes.server,
    blockTitleIconClass: "fas fa-server mr-2",
    loading: state.peaks.filters.hierarchy.loading,
    error: state.peaks.filters.hierarchy.error
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
