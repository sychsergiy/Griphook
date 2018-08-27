import React from "react";
import { connect } from "react-redux";

import { selectPeaksTarget } from "../../options/actions";

import {
  selectClusterFilter,
  unSelectClusterFilter
} from "../actions/selections";

import { separateSelectedItems } from "../../../common/filtersHelper/common";

import { peaksTargetTypes } from "../../../common/constants";

import FilterContainer from "./FilterContainer";

const mapStateToProps = state => {
  let [selectedClusters, visibleClusters] = separateSelectedItems(
    state.peaks.filters.hierarchy.clusters,
    state.peaks.filters.selections.clusters
  );
  // Target - item for displaying charts
  // item with selected TargetID need to be active
  // allItems - for search but, now uneeded to remove, because search will be by visibleItems
  // selectedItems - map li with - icon
  // visibleItems - map li with + icon

  return {
    visibleItems: visibleClusters,
    selectedItems: selectedClusters,
    blockTitle: "Clusters",

    selectedTargetID: state.peaks.chartsOptions.targetID,
    selectedTargetType: state.peaks.chartsOptions.targetType,
    currentTargetType: peaksTargetTypes.cluster,
    blockTitleIconClass: "fas fa-th-large"
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
    dispatch(selectPeaksTarget(targetID, peaksTargetTypes.cluster));
  }
});

const ClusterFilterContainer = connect(
  mapStateToProps,
  mapDispatchToProps
)(FilterContainer);

export default ClusterFilterContainer;
