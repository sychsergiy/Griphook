import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchGroupServicesData } from "../actions/services";

import { Spinner } from "../../../common/spinner";

import ServicesTableComponent from "../components/servicesTable";

class ServicesTableContainer extends Component {
  componentDidMount() {
    this.props.fetchTableData(this.props.requestOptions);
  }
  render() {
    if (this.props.loading) {
      return <Spinner />;
    }

    if (this.props.error) {
      return this.props.error.toString();
    }

    return <ServicesTableComponent services={this.props.services} />;
  }
}

const mapStateToProps = state => ({
  requestOptions: {
    time_from: state.billing.options.timeFrom.format("YYYY-MM-DD"),
    time_until: state.billing.options.timeUntil.format("YYYY-MM-DD"),
    services_group_id: state.billing.table.groups.selectedItemID
  },

  error: state.billing.table.groupServices.error,
  loading: state.billing.table.groupServices.loading,
  services: state.billing.table.groupServices.items
});

const mapDispatchToProps = dispatch => ({
  fetchTableData: options => {
    dispatch(fetchGroupServicesData(options));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServicesTableContainer);
