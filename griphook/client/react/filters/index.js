import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchFiltersHierarchy } from "./actions/hierarchy";
import ClusterFilterContainer from "./containers/ClusterFilter";
import ServerFilterContainer from "./containers/ServerFilter";
import ServicesGroupFilterContainer from "./containers/ServicesGroupFilter";
import ServiceFilterContainer from "./containers/ServiceFilter";

class Filters extends Component {
  componentDidMount() {
    this.props.dispatch(fetchFiltersHierarchy());
  }

  render() {
    if (this.props.error) {
      return <div>Error! {this.props.error.message}</div>;
    }

    if (this.props.loading) {
      return <div>Loading...</div>;
    }
    return (
      <div className="col-xl-3 col-lg-4 col-md-4 col-sm-12 filters text-center">
        <ClusterFilterContainer />
        <ServerFilterContainer />
        <ServicesGroupFilterContainer />
        <ServiceFilterContainer />
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    loading: state.filters.hierarchy.loading,
    error: state.filters.hierarchy.error
  };
};

export default connect(mapStateToProps)(Filters);
