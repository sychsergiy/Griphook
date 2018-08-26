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
    this.setState({ searchQuery });
  }

  setPageNumber(pageNumber) {
    this.setState({ pageNumber });
  }

  getSelectedTargetIDs() {
    // check IDs only if target_type equals to current
    if (this.props.currentTargetType === this.props.selectedTargetType) {
      return this.props.selectedTargetIDs;
    } else return [];
  }

  render() {
    let visibleItems;
    if (this.state.searchQuery) {
      visibleItems = this.props.visibleItems.filter(item =>
        item.title.includes(this.state.searchQuery)
      );
    } else visibleItems = this.props.visibleItems;

    let page = paginator(visibleItems).getPage(this.state.pageNumber);

    return (
      <FilterBlockComponent
        page={page}
        setPageNumber={this.setPageNumber}
        blockTitle={this.props.blockTitle}
        onSearchInputChange={this.onSearchInputChange}
        onTargetClick={this.props.selectTarget}
        selectedTargetIDs={this.getSelectedTargetIDs()}
        selectedItems={this.props.selectedItems}
        onSelectFilterItem={this.props.selectFilterItem}
        onUnselectFilterItem={this.props.unSelectFilterItem}
        multiselect={this.props.multiselect}
        hideIcon={this.props.hideIcon}
      />
    );
  }
}
