import React, { Component } from "react";
import { connect } from "react-redux";

import { paginator } from "../../../common/paginator";

import { FilterBlockComponent } from "../components/filterBlock";

export default class BaseFilterContainer extends Component {
  constructor(props) {
    super();
    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.incrementPageNumber = this.incrementPageNumber.bind(this);
    this.decrementPageNumber = this.decrementPageNumber.bind(this);
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedItems = this.props.allItems.filter(item =>
      item.title.includes(searchQuery)
    );
    console.log(findedItems);
  }

  incrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber + 1);
  }

  decrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber - 1);
  }

  getSelectedItemIDs() {
    // check IDs only if target_type equals to current
    if (this.props.currentTargetType === this.props.selectedTargetType) {
      return this.props.selectedTargetIDs;
    } else return [];
  }

  render() {
    let page = paginator(this.props.visibleItems).getPage(
      this.props.pageNumber
    );

    return (
      <div>
        <FilterBlockComponent
          items={page.items}
          blockTitle={this.props.blockTitle}
          onSearchInputChange={this.onSearchInputChange}
          onItemClick={this.props.selectTarget}
          selectedItemIDs={this.getSelectedItemIDs()}
          multiselect={this.props.multiselect}
        />
        {page.previousPageExists ? (
          <div onClick={this.decrementPageNumber}>Previous Page</div>
        ) : null}

        {page.nextPageExists ? (
          <div onClick={this.incrementPageNumber}>Next Page</div>
        ) : null}
      </div>
    );
  }
}
