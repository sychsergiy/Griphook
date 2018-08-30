import React, { Component } from "react";

import ListBlockComponent from "../components/listBlock";
import InputBlockContainer from "./InputBlock";

import { listDataType } from "../constants";
import { Spinner } from "../../../../common/spinner";
import { getErrorInformation } from "../../../resources/utils";
import { createObject, deleteObject, getObjects } from "../requestHelpers";

class ModalBodyContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      listData: [],
      loading: false
    };
    this.onRowDelete = this.onRowDelete.bind(this);
    this.onRowAdd = this.onRowAdd.bind(this);
  }

  componentDidMount() {
    this.setState({ loading: true });
    getObjects(this.props.listDataType).then(response => {
      if (response.ok) {
        response.json().then(data => {
          if (this.props.listDataType === listDataType.projects) {
            this.setState({ listData: data.projects, loading: false });
          } else if (this.props.listDataType === listDataType.teams) {
            this.setState({ listData: data.teams, loading: false });
          }
        });
      } else {
        response.json().then(data => {
          // TODO: output !data.error!
          alert(getErrorInformation(data.error));
          this.setState({ loading: false });
        });
      }
    });
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.listDataType !== this.props.listDataType) {
      getObjects(nextProps.listDataType).then(response => {
        if (response.ok) {
          response.json().then(data => {
            if (nextProps.listDataType === listDataType.projects) {
              this.setState({ listData: data.projects, loading: false });
            } else if (nextProps.listDataType === listDataType.teams) {
              this.setState({ listData: data.teams, loading: false });
            }
          });
        } else {
          response.json().then(data => {
            // TODO: output !data.error!
            alert(getErrorInformation(data.error));
            this.setState({ loading: false });
          });
        }
      });
    }
  }

  onRowDelete(objectId) {
    this.setState({ loading: true });
    deleteObject(this.props.listDataType, objectId).then(response => {
      if (response.ok) {
        response.json().then(() => {
          const rowObject = this.state.listData.find(
            object => object.id === objectId
          );
          const objectIndex = this.state.listData.indexOf(rowObject);

          this.setState({
            listData: [
              ...this.state.listData.slice(0, objectIndex),
              ...this.state.listData.slice(objectIndex + 1)
            ],
            loading: false
          });
        });
      } else {
        console.log(response.json());
        response.json().then(data => {
          // TODO: output !data.error!
          alert(getErrorInformation(data.error));
          this.setState({ loading: false });
        });
      }
    });
  }

  onRowAdd(objectTitle) {
    this.setState({ loading: true });
    createObject(this.props.listDataType, objectTitle).then(response => {
      if (response.ok) {
        response.json().then(object => {
          const newRow = { id: object.id, title: object.title };

          this.setState({
            listData: [...this.state.listData, newRow],
            loading: false
          });
        });
      } else {
        response.json().then(data => {
          // TODO: output !data.error!
          alert(getErrorInformation(data.error));
          this.setState({ loading: false });
        });
      }
    });
  }
  render() {
    if (this.state.loading === true) {
      return <Spinner />;
    }
    return (
      <div className="modal-body">
        <div className="row">
          <InputBlockContainer onRowAdd={this.onRowAdd} />
          <ListBlockComponent
            listData={this.state.listData}
            onRowDelete={this.onRowDelete}
          />
        </div>
      </div>
    );
  }
}

export default ModalBodyContainer;
