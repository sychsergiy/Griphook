import React, { Component } from "react";
import { connect } from "react-redux";

import { setTargetOption } from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import {
  selectServerFilter,
  unSelectServerFilter
} from "../actions/selections";

import { getFilteredServers } from "../../../common/filtersHelper/servers";
import { separateSelectedItems } from "../../../common/filtersHelper/common";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => {
  let [selectedServers, unSelectedServers] = separateSelectedItems(
    state.billing.filters.hierarchy.servers,
    state.billing.filters.selections.servers
  );
  let filteredServers = getFilteredServers(
    state.billing.filters.selections,
    unSelectedServers
  );
  return {
    selectedItems: selectedServers,
    visibleItems: filteredServers, // paginator
    currentTargetType: billingTargetTypes.server,
    selectedTargetType: state.billing.options.targetType,
    selectedTargetIDs: state.billing.options.targetIDs,
    blockTitle: "Servers",
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
    dispatch(setTargetOption(targetID, billingTargetTypes.server));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
