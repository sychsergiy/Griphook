import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchBillingTableData } from "../actions/groups";

import {
  selectBillingTableRow,
  unSelectBillingTableRow
} from "../actions/groups";

import { isEquivalent } from "../../../common/utils";

import BillingTableComponent from "../components/billingTable";

class BillingTableContainer extends Component {
  componentDidMount() {
    this.props.fetchTableData(this.props.requestOptions);
    this.onExpandButtonClick = this.onExpandButtonClick.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (!isEquivalent(this.props.requestOptions, nextProps.requestOptions)) {
      this.props.fetchTableData(nextProps.requestOptions);
    }
  }

  onExpandButtonClick(servicesGroupID) {
    if (this.props.selectedGroupID === servicesGroupID) {
      this.props.hideRow();
    } else this.props.expandRow(servicesGroupID);
  }

  render() {
    if (this.props.loading) {
      return <div>Loading ...</div>;
    }
    if (this.props.error) {
      return <div>{this.props.error.toString()}</div>;
    }

    return (
      <BillingTableComponent
        selectedGroupID={this.props.selectedGroupID}
        groups={this.props.servicesGroups}
        onExpandButtonClick={this.onExpandButtonClick}
      />
    );
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.billing.options.timeFrom.format("YYYY-MM-DD"),
    time_until: state.billing.options.timeUntil.format("YYYY-MM-DD"),
    target_ids: state.billing.options.targetIDs,
    target_type: state.billing.options.targetType
  },

  loading: state.billing.table.groups.loading,
  error: state.billing.table.groups.error,
  servicesGroups: state.billing.table.groups.items,
  selectedGroupID: state.billing.table.groups.selectedItemID
});
const mapDispatchToProps = dispatch => ({
  fetchTableData: options => {
    dispatch(fetchBillingTableData(options));
  },
  expandRow: servicesGroupID => {
    dispatch(selectBillingTableRow(servicesGroupID));
  },
  hideRow: () => {
    dispatch(unSelectBillingTableRow());
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BillingTableContainer);
