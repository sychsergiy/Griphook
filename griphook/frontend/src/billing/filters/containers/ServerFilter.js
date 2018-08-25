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
    blockTitle: "Servers"
  };
};

const mapDispatchToProps = dispatch => ({
  selectFilterItem: clusterID => {
    dispatch(selectServerFilter(clusterID));
  },
  unSelectFilterItem: clusterID => {
    dispatch(unSelectServerFilter(clusterID));
  },
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.server));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
