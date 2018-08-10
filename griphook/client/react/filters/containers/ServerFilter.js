import React, { Component } from "react";
import { connect } from "react-redux";

import { FilterBlockComponent } from "../components/filterBlock";
import { getFilteredServers } from "../serversHelper";

import {
  selectServerFilter,
  unselectServerFilter
} from "../actions/selections";
import {
  setServersFilterPageNumber,
  setServicesGroupsFilterPageNumber,
  setServicesFilterPageNumber
} from "../actions/pagination";

import { separateSelectedItems, paginator } from "../common";

class ServerFilterContainer extends Component {
  constructor(props) {
    super();
    this.toggleServerFilter = this.toggleServerFilter.bind(this);
    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.incrementPageNumber = this.incrementPageNumber.bind(this);
    this.decrementPageNumber = this.decrementPageNumber.bind(this);
  }

  toggleServerFilter(event) {
    this.props.resetFiltersPagination();
    if (event.target.checked) {
      this.props.selectServer(event.target.value);
    } else {
      this.props.unselectServer(event.target.value);
    }
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedServers = this.props.allServers.filter(server =>
      server.title.includes(searchQuery)
    );
    console.log(findedServers);
  }

  incrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber + 1);
  }

  decrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber - 1);
  }

  render() {
    let page = paginator(this.props.filteredServers).getPage(
      this.props.pageNumber
    );

    return (
      <div>
        <FilterBlockComponent
          selectedItems={this.props.selectedServers}
          items={page.items}
          blockTitle="Server"
          onSearchInputChange={this.onSearchInputChange}
          onFilterToggle={this.toggleServerFilter}
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
  let allServers = state.filters.hierarchy.servers;
  let selections = state.filters.selections;
  const pageNumber = state.filters.pagination.serversPageNumber;
  let [selectedServers, visibleServers] = separateSelectedItems(
    allServers,
    selections.servers
  );
  let filteredServers = getFilteredServers(selections, visibleServers);
  return { allServers, selectedServers, filteredServers, pageNumber };
};
const mapDispatchToProps = dispatch => ({
  selectServer: serverID => {
    dispatch(selectServerFilter(serverID));
  },
  unselectServer: serverID => {
    dispatch(unselectServerFilter(serverID));
  },
  setPageNumber: pageNumber => {
    dispatch(setServersFilterPageNumber(pageNumber));
  },
  resetFiltersPagination: () => {
    // reset pagination for all filters lower than Server
    dispatch(setServicesGroupsFilterPageNumber(0));
    dispatch(setServicesFilterPageNumber(0));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServerFilterContainer);
