import React, { Component } from "react";
import { connect } from "react-redux";

import { paginator } from "../../../common/paginator";

import { FilterBlockComponent } from "../components/filterBlock";

export default class BaseFilterContainer extends Component {
  constructor(props) {
    super();
    this.state = {
      pageNumber: 1,
      searchQuery: ""
    };

    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.setPageNumber = this.setPageNumber.bind(this);
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedItems = this.props.allItems.filter(item =>
      item.title.includes(searchQuery)
    );
    console.log(findedItems);
  }

  setPageNumber(pageNumber) {
    this.setState({ pageNumber });
  }

  getSelectedItemIDs() {
    // check IDs only if target_type equals to current
    if (this.props.currentTargetType === this.props.selectedTargetType) {
      return this.props.selectedTargetIDs;
    } else return [];
  }

  render() {
    let page = paginator(this.props.visibleItems).getPage(
      this.state.pageNumber
    );

    return (
      <FilterBlockComponent
        page={page}
        setPageNumber={this.setPageNumber}
        blockTitle={this.props.blockTitle}
        onSearchInputChange={this.onSearchInputChange}
        onItemClick={this.props.selectTarget}
        selectedItemIDs={this.getSelectedItemIDs()}
        multiselect={this.props.multiselect}
      />
    );
  }
}
