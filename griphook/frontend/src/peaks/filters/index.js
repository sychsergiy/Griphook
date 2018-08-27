import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchFiltersHierarchy } from "./actions/hierarchy";
import ClusterFilterContainer from "./containers/ClusterFilter";
import ServerFilterContainer from "./containers/ServerFilter";
import ServicesGroupFilterContainer from "./containers/ServicesGroupFilter";
import ServiceFilterContainer from "./containers/ServiceFilter";

const PeaksFiltersComponent = props => (
  <div className="filter-group flex-grow-0 flex-shrink-0 mx-md-1 mx-lg-4">
    <div className="row">
      <ClusterFilterContainer />
      <ServerFilterContainer />
      <ServicesGroupFilterContainer />
      <ServiceFilterContainer />
    </div>
  </div>
);

class PeaksFiltersContainer extends Component {
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
    return <PeaksFiltersComponent />;
  }
}

const mapStateToProps = state => {
  return {
    loading: state.peaks.filters.hierarchy.loading,
    error: state.peaks.filters.hierarchy.error
  };
};

export default connect(mapStateToProps)(PeaksFiltersContainer);
