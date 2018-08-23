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
      <div>
        <ProjectFilterContainer />
        <TeamFilterContainer />
        <ClusterFilterContainer />
        <ServerFilterContainer />
        <GroupFilterContainer />
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
