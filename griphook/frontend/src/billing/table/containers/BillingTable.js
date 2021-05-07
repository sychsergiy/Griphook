import React, { Component } from "react";
import { connect } from "react-redux";

import {
  fetchBillingTableData,
  setBillingTablePageNumber
} from "../actions/groups";

import {
  selectBillingTableRow,
  unSelectBillingTableRow
} from "../actions/groups";

import { isEquivalent } from "../../../common/utils";

import { Spinner } from "../../../common/spinner";

import BillingTableComponent from "../components/billingTable";

class BillingTableContainer extends Component {
  componentDidMount() {
    this.props.fetchTableData(this.props.requestOptions);
    this.onExpandButtonClick = this.onExpandButtonClick.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (!isEquivalent(this.props.requestOptions, nextProps.requestOptions)) {
      if (this.props.requestOptions.page === nextProps.requestOptions.page) {
        this.props.setPageNumber(1);
        nextProps.requestOptions.page = 1;
      }
      this.props.fetchTableData(nextProps.requestOptions);
    }
  }

  onExpandButtonClick(servicesGroupID) {
    if (this.props.selectedGroupID === servicesGroupID) {
      this.props.hideRow();
    } else this.props.expandRow(servicesGroupID);
  }

  render() {
    return (
      <BillingTableComponent
        selectedGroupID={this.props.selectedGroupID}
        groups={this.props.servicesGroups}
        onExpandButtonClick={this.onExpandButtonClick}
        loading={this.props.loading}
        error={this.props.error}
      />
    );
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    page: state.billing.table.groups.pageNumber,
    time_from: state.billing.options.timeFrom.format("YYYY-MM-DD"),
    time_until: state.billing.options.timeUntil.format("YYYY-MM-DD"),
    target_ids: state.billing.options.targetIDs,
    target_type: state.billing.options.targetType
  },

  loading: state.billing.table.groups.loading,
  error: state.billing.table.groups.error,
  servicesGroups: state.billing.table.groups.pageItems,
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
  },
  setPageNumber: pageNumber => {
    dispatch(setBillingTablePageNumber(pageNumber));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BillingTableContainer);
