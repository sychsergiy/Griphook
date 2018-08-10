import React, { Component } from "react";
import { connect } from "react-redux";

import { FilterBlockComponent } from "../components/filterBlock";

import {
  selectClusterFilter,
  unselectClusterFilter
} from "../actions/selections";

import {
  setClustersPageNumber,
  setServersFilterPageNumber,
  setServicesGroupsFilterPageNumber,
  setServicesFilterPageNumber
} from "../actions/pagination";

import { separateSelectedItems, paginator } from "../common.js";

class ClusterFilterContainer extends Component {
  constructor(props) {
    super();
    this.toggleClusterFilter = this.toggleClusterFilter.bind(this);
    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.incrementPageNumber = this.incrementPageNumber.bind(this);
    this.decrementPageNumber = this.decrementPageNumber.bind(this);
  }

  toggleClusterFilter(event) {
    this.props.resetFiltersPagination();
    if (event.target.checked) {
      this.props.selectCluster(event.target.value);
    } else {
      this.props.unselectCluster(event.target.value);
    }
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedClusters = this.props.allClusters.filter(cluster =>
      cluster.title.includes(searchQuery)
    );
    console.log(findedClusters);
  }

  incrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber + 1);
  }

  decrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber - 1);
  }

  render() {
    let page = paginator(this.props.visibleClusters).getPage(
      this.props.pageNumber
    );
    return (
      <div>
        <FilterBlockComponent
          selectedItems={this.props.selectedClusters}
          items={page.items}
          onFilterToggle={this.toggleClusterFilter}
          onSearchInputChange={this.onSearchInputChange}
          blockTitle="Cluster"
        />
        {page.previousPageExists() ? (
          <div onClick={this.decrementPageNumber}>Previous Page</div>
        ) : null}

        {page.nextPageExists() ? (
          <div onClick={this.incrementPageNumber}>Next Page</div>
        ) : null}
      </div>
    );
  }
}

const mapStateToProps = state => {
  let allClusters = state.filters.hierarchy.clusters;
  const pageNumber = state.filters.pagination.clustersPageNumber;
  let [selectedClusters, visibleClusters] = separateSelectedItems(
    allClusters,
    state.filters.selections.clusters
  );
  return {
    visibleClusters,
    selectedClusters,
    allClusters,
    pageNumber
  };
};

const mapDispatchToProps = dispatch => ({
  selectCluster: clusterID => {
    dispatch(selectClusterFilter(clusterID));
  },
  unselectCluster: clusterID => {
    dispatch(unselectClusterFilter(clusterID));
  },
  setPageNumber: pageNumber => {
    dispatch(setClustersPageNumber(pageNumber));
  },
  resetFiltersPagination: () => {
    // reset pagination for all filters lower than Cluster
    dispatch(setServersFilterPageNumber(0));
    dispatch(setServicesGroupsFilterPageNumber(0));
    dispatch(setServicesFilterPageNumber(0));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ClusterFilterContainer);
