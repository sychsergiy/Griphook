import React, { Component } from "react";
import { connect } from "react-redux";

import { setTargetOption } from "../../options/actions";

import {
  selectClusterFilter,
  unSelectClusterFilter
} from "../actions/selections";

import { separateSelectedItems } from "../../../common/filtersHelper/common";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

const mapStateToProps = state => {
  let [selectedClusters, unSelectedClusters] = separateSelectedItems(
    state.billing.filters.hierarchy.clusters,
    state.billing.filters.selections.clusters
  );
  return {
    selectedItems: selectedClusters,
    visibleItems: unSelectedClusters,
    currentTargetType: billingTargetTypes.cluster,
    selectedTargetType: state.billing.options.targetType,
    selectedTargetIDs: state.billing.options.targetIDs,
    blockTitle: "Clusters",
    blockTitleIconClass: "fas fa-th-large mr-2",
    loading: state.billing.filters.hierarchy.loading,
    error: state.billing.filters.hierarchy.error
  };
};

const mapDispatchToProps = dispatch => ({
  selectFilterItem: clusterID => {
    dispatch(selectClusterFilter(clusterID));
  },
  unSelectFilterItem: clusterID => {
    dispatch(unSelectClusterFilter(clusterID));
  },
  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.cluster));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BaseFilterContainer);
