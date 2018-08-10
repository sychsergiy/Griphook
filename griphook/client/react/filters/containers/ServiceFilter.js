import React, { Component } from "react";
import { connect } from "react-redux";

import { FilterBlockComponent } from "../components/filterBlock";
import { getFilteredServices } from "../servicesHelper";

import { setServicesFilterPageNumber } from "../actions/pagination";

import { paginator } from "../common";

class ServiceFilterContainer extends Component {
  constructor(props) {
    super();
    this.onSearchInputChange = this.onSearchInputChange.bind(this);
    this.incrementPageNumber = this.incrementPageNumber.bind(this);
    this.decrementPageNumber = this.decrementPageNumber.bind(this);
  }

  onSearchInputChange(event) {
    const searchQuery = event.target.value;
    let findedServices = this.props.allServices.filter(service =>
      service.title.includes(searchQuery)
    );
    console.log(findedServices);
  }

  incrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber + 1);
  }

  decrementPageNumber() {
    this.props.setPageNumber(this.props.pageNumber - 1);
  }

  render() {
    let page = paginator(this.props.filteredServices).getPage(
      this.props.pageNumber
    );
    return (
      <div>
        <FilterBlockComponent
          selectedItems={[]} // todo: do I really need multichoice for services - no!
          items={page.items}
          onSearchInputChange={this.onSearchInputChange}
          blockTitle="Services"
        />
        {page.previousPageExists() ? (
          <div onClick={this.decrementPageNumber}>Previous Page</div>
        ) : null}
        {page.nextPageExists() ? (
          <div onClick={this.incrementPageNumber}>Next Page</div>
        ) : null}
      </div>
    );
  }
}
const mapStateToProps = state => ({
  allServices: state.filters.hierarchy.services,
  pageNumber: state.filters.pagination.servicesPageNumber,
  filteredServices: getFilteredServices(
    state.filters.selections,
    state.filters.hierarchy.services
  )
});

const mapDispatchToProps = dispatch => ({
  setPageNumber: pageNumber => {
    dispatch(setServicesFilterPageNumber(pageNumber));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ServiceFilterContainer);
