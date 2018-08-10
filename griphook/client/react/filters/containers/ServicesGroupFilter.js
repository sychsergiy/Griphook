import React, { Component } from "react";
import { connect } from "react-redux";

import { FilterBlockComponent } from "../components/filterBlock";
import { getFilteredServicesGroups } from "../servicesGroupsHelper";

import {
  selectServicesGroupFilter,
  unselectServicesGroupFilter
} from "../actions/selections";
import {
  setServicesGroupsFilterPageNumber,
  setServicesFilterPageNumber
} from "../actions/pagination";

import { separateSelectedItems, paginator } from "../common.js";

class ServicesGroupFilterContainer extends Component {
  constructor(props) {
    super();
    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.toggleServicesGroupFilter = this.toggleServicesGroupFilter.bind(this);
    this.incrementPageNumber = this.incrementPageNumber.bind(this);
    this.decrementPageNumber = this.decrementPageNumber.bind(this);
  }

  toggleServicesGroupFilter(event) {
    this.props.resetFiltersPagination();
    if (event.target.checked) {
      this.props.selectServicesGroup(event.target.value);
    } else {
      this.props.unselectServicesGroup(event.target.value);
    }
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedGroups = this.props.allGroups.filter(group =>
      group.title.includes(searchQuery)
    );
    console.log(findedGroups);
  }

  incrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber + 1);
  }

  decrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber - 1);
  }

  render() {
    let page = paginator(this.props.filteredGroups).getPage(
      this.props.pageNumber
    );
    return (
      <div>
        <FilterBlockComponent
          selectedItems={this.props.selectedGroups}
          items={page.items}
          onFilterToggle={this.toggleServicesGroupFilter}
          onSearchInputChange={this.onSearchInputChange}
          blockTitle="Groups"
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
  let allGroups = state.filters.hierarchy.servicesGroups;
  let selections = state.filters.selections;
  const pageNumber = state.filters.pagination.servicesGroupsPageNumber;
  let [selectedGroups, visibleGroups] = separateSelectedItems(
    allGroups,
    selections.servicesGroups
  );

  let filteredGroups = getFilteredServicesGroups(selections, visibleGroups);
  return {
    allGroups,
    selectedGroups,
    filteredGroups,
    pageNumber
  };
};

const mapDispatchToProps = dispatch => ({
  selectServicesGroup: servicesGroupID => {
    dispatch(selectServicesGroupFilter(servicesGroupID));
  },
  unselectServicesGroup: servicesGroupID => {
    dispatch(unselectServicesGroupFilter(servicesGroupID));
  },
  setPageNumber: pageNumber => {
    dispatch(setServicesGroupsFilterPageNumber(pageNumber));
  },
  resetFiltersPagination: () => {
    // reset pagination for all filters lower than ServicesGroup
    dispatch(setServicesFilterPageNumber(0));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServicesGroupFilterContainer);
