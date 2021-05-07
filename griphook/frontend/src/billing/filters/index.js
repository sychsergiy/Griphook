import React, { Component } from "react";
import { connect } from "react-redux";

import { fetchBillingFiltersHierarchy } from "./actions/hierarchy";

import ProjectFilterContainer from "./containers/ProjectFilter";
import TeamFilterContainer from "./containers/TeamFilter";
import ClusterFilterContainer from "./containers/ClusterFilter";
import ServerFilterContainer from "./containers/ServerFilter";
import GroupFilterContainer from "./containers/GroupFilter";

class BillingFiltersContainer extends Component {
  componentDidMount() {
    this.props.fetchFiltersHierarchy();
  }

  render() {
    return (
      <div className="filter-group flex-grow-0 flex-shrink-0 mx-md-1 mx-lg-4">
        <div className="row">
          <ProjectFilterContainer />
          <TeamFilterContainer />
          <ClusterFilterContainer />
          <ServerFilterContainer />
          <GroupFilterContainer />
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => ({});
const mapDispatchToProps = dispatch => ({
  fetchFiltersHierarchy: () => {
    dispatch(fetchBillingFiltersHierarchy());
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(BillingFiltersContainer);
