import React, { Component } from "react";
import { connect } from "react-redux";

import { setServicesGroupsFilterPageNumber } from "../actions/pagination";
import {
  setTargetOption,
  addGroupToTargetIDs,
  removeGroupFromTargetIDs
} from "../../options/actions";

import { billingTargetTypes } from "../../../common/constants";

import BaseFilterContainer from "./BaseFilter";

class ServicesGroupFilterContainer extends Component {
  constructor(props) {
    super();
    this.toggleFilterItem = this.toggleFilterItem.bind(this);
  }

  toggleFilterItem(groupID) {
    if (this.props.selectedTargetType !== this.props.currentTargetType) {
      // add to target_ids and set new target type (old action)
      this.props.selectTarget(groupID);
    } else {
      if (!this.props.selectedTargetIDs.includes(groupID)) {
        // add id to targetIDs
        this.props.selectGroup(groupID);
      } else {
        // cancel unSelecting last targetID,
        // because server will return bad request
        // need to set targetType equals "all"
        if (this.props.selectedTargetIDs.length !== 1) {
          // remove from target_ids
          this.props.unSelectGroup(groupID);
        }
      }
    }
  }

  render() {
    return (
      <BaseFilterContainer
        allItems={this.props.allItems}
        visibleItems={this.props.visibleItems}
        pageNumber={this.props.pageNumber}
        currentTargetType={this.props.currentTargetType}
        selectedTargetType={this.props.selectedTargetType}
        selectedTargetIDs={this.props.selectedTargetIDs}
        blockTitle={this.props.blockTitle}
        setPageNumber={this.props.setPageNumber}
        selectTarget={this.toggleFilterItem}
        multiselect={true}
      />
    );
  }
}

const mapStateToProps = state => ({
  allItems: state.billing.filters.hierarchy.servicesGroups,
  visibleItems: state.billing.filters.hierarchy.servicesGroups,
  pageNumber: state.billing.filters.pagination.servicesGroupsPageNumber,
  currentTargetType: billingTargetTypes.group,
  selectedTargetType: state.billing.options.targetType,
  selectedTargetIDs: state.billing.options.targetIDs,
  blockTitle: "Services Groups"
});

const mapDispatchToProps = dispatch => ({
  setPageNumber: pageNumber => {
    dispatch(setServicesGroupsFilterPageNumber(pageNumber));
  },

  selectGroup: groupID => {
    dispatch(addGroupToTargetIDs(groupID));
  },
  unSelectGroup: groupID => {
    dispatch(removeGroupFromTargetIDs(groupID));
  },

  selectTarget: targetID => {
    dispatch(setTargetOption(targetID, billingTargetTypes.group));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServicesGroupFilterContainer);
