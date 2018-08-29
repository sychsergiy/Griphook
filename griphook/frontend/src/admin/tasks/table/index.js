import React, { Component } from "react";

import TableBodyComponent from "./components/tableBody";
import TableHeaderComponent from './components/tableHeader'

import {TableSpinnerComponent} from "../../common/tableSpinner";
import {TableControlPanelComponent} from "./components/tableControlPanel"
import {TablePaginationComponent} from "./components/tablePagination"
import {paginator} from "./paginator"

import {
  fetchServicesgroupsProjectsTeams,
  attachProject,
  attachTeam
} from "./fetchHelpers";


class TableContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      servicesGroups: [],
      servicesGroupsFiltered: [],
      projects: [],
      teams: [],
      pageNumber: 1,
      loading: false
    };
    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.attachProjectToServicesGroup = this.attachProjectToServicesGroup.bind(this);
    this.attachTeamToServicesGroup = this.attachTeamToServicesGroup.bind(this);

    this.setPageNumber = this.setPageNumber.bind(this);
    this.incrementPageNumber = this.incrementPageNumber.bind(this);
    this.decrementPageNumber = this.decrementPageNumber.bind(this);
  }

  componentDidMount() {
    this.setState({loading: true});
    fetchServicesgroupsProjectsTeams().then(response => {
      if (response.ok) {
        response.json().then(data => {
          this.setState({
            servicesGroups: data.services_groups,
            servicesGroupsFiltered: data.services_groups,
            projects: data.projects,
            teams: data.teams,
            loading: false
          });
        });
      } else {
        response.json().then(data => {
          // TODO: output !data.error!
          this.setState({ loading: false });
        });
      }
    });
  }

  setPageNumber(pageNumber) {
    this.setState({ pageNumber: pageNumber });
  }
  incrementPageNumber() {
    this.setPageNumber(this.state.pageNumber + 1);
  }
  decrementPageNumber() {
    this.setPageNumber(this.state.pageNumber - 1);
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedItems = this.state.servicesGroups.filter(item =>
      item.title.includes(searchQuery)
    );
    this.setState({ servicesGroupsFiltered: findedItems });
  }

  attachTeamToServicesGroup(event, servicesGroupId) {
    const newTeamId = parseInt(event.target.value);
    this.setState({loading: true});
    attachTeam(newTeamId, servicesGroupId)
    .then(() => {
      const ServicesGroupObject = this.state.servicesGroups.find(object => object.id === servicesGroupId);
      const objectIndex = this.state.servicesGroups.indexOf(ServicesGroupObject);

      let servicesGroups = [...this.state.servicesGroups];
      servicesGroups[objectIndex].team_id=newTeamId;

      this.setState({servicesGroups: servicesGroups, loading: false});
    });
  }

  attachProjectToServicesGroup(event, servicesGroupId) {
    const newProjectId = parseInt(event.target.value);
    this.setState({loading: true});
    attachProject(newProjectId, servicesGroupId)
    .then(() => {
      const ServicesGroupObject = this.state.servicesGroups.find(object => object.id === servicesGroupId);
      const objectIndex = this.state.servicesGroups.indexOf(ServicesGroupObject);

      let servicesGroups = [...this.state.servicesGroups];
      servicesGroups[objectIndex].project_id=newProjectId;

      this.setState({servicesGroups: servicesGroups, loading: false});
    });
  }

  render() {
    if (this.state.loading === true) {
      return (
        <div>
          <TableControlPanelComponent
            onSearchInputChange={this.onSearchInputChange}
            showModal={this.props.showModal} />
          <table className="table mt-2">
            <TableHeaderComponent />
            <TableSpinnerComponent />
          </table>
        </div>
      );
    }

    let page = paginator(this.state.servicesGroupsFiltered, this.state.pageNumber);
    let dataAfterPagination = page.items

    return (
      <div>
        <TableControlPanelComponent
          onSearchInputChange={this.onSearchInputChange}
          showModal={this.props.showModal} />
        <table className="table mt-2">
          <TableHeaderComponent />
          <TableBodyComponent
            dataAfterPagination={dataAfterPagination}
            projects={this.state.projects}
            teams={this.state.teams}
            attachProjectToServicesGroup={this.attachProjectToServicesGroup}
            attachTeamToServicesGroup={this.attachTeamToServicesGroup}
            />
        </table>
        <TablePaginationComponent
          page={page}
          pageNumber={this.state.pageNumber}
          incrementPageNumber={this.incrementPageNumber}
          decrementPageNumber={this.decrementPageNumber}
          />
      </div>
    );
  }
}

export default TableContainer;
