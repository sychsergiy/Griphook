import React, { Component } from "react";

import {fetchClusters, updateClusterCPUPrice, updateClusterMemoryPrice} from "../fetchHelpers";
import {TableClustersRowComponent} from "../components/tableClustersRow";
import {getErrorInformation} from "../utils";
import {TableSpinnerComponent} from "../../common/tableSpinner";


class TableClustersBodyContainer extends Component {
   constructor(props) {
    super(props);
    this.state = {
      tableData: [],
      loading: false
    };
    this.renderTableRows = this.renderTableRows.bind(this);
    this.clusterUpdateCPUPrice = this.clusterUpdateCPUPrice.bind(this);
    this.clusterUpdateMemoryPrice = this.clusterUpdateMemoryPrice.bind(this);
  }

  componentDidMount() {
    this.setState({loading: true});
    fetchClusters().then(response => {
      if (response.ok) {
        response.json().then(data => {
            this.setState({ tableData: data.clusters, loading: false});
        });
      } else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
            this.setState({loading: false});
        });
      }
    });
  }

  clusterUpdateCPUPrice(clusterId, clusterCPUPrice) {
    this.setState({loading: true});
    updateClusterCPUPrice(clusterId, clusterCPUPrice).then(response => {
      if (response.ok) {
          if (isNaN(clusterCPUPrice)) {clusterCPUPrice = ''}
          const clusterObject = this.state.tableData.find(object => object.id === clusterId);
          const objectIndex = this.state.tableData.indexOf(clusterObject);

          let tableData = [...this.state.tableData];
          tableData[objectIndex] = { id: clusterId, title: clusterObject.title, cpu_price: clusterCPUPrice, memory_price: clusterObject.memory_price};

          this.setState({tableData: tableData, loading: false});
      }
      else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
            this.setState({loading: false});
        });
      }
    });
  }

  clusterUpdateMemoryPrice(clusterId, clusterMemoryPrice) {
    this.setState({loading: true});
    updateClusterMemoryPrice(clusterId, clusterMemoryPrice).then(response => {
      if (response.ok) {
          if (isNaN(clusterMemoryPrice)) {clusterMemoryPrice = ''}
          const clusterObject = this.state.tableData.find(object => object.id === clusterId);
          const objectIndex = this.state.tableData.indexOf(clusterObject);

          let tableData = [...this.state.tableData];
          tableData[objectIndex] = { id: clusterId, title: clusterObject.title, cpu_price: clusterObject.cpu_price, memory_price: clusterMemoryPrice};

          this.setState({tableData: tableData, loading: false});
      }
      else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
            this.setState({loading: false});
        });
      }
    });
  }

  renderTableRows(clusters) {
    return clusters.map(cluster => {
        if (cluster.cpu_price === null) {cluster.cpu_price = ''}
        if (cluster.memory_price === null) {cluster.memory_price = ''}
      return (
          <TableClustersRowComponent
            key={cluster.id}
            clusterId={cluster.id}
            clusterTitle={cluster.title}
            clusterCPUPrice={cluster.cpu_price}
            clusterMemoryPrice={cluster.memory_price}
            clusterUpdateCPUPrice={this.clusterUpdateCPUPrice}
            clusterUpdateMemoryPrice={this.clusterUpdateMemoryPrice}
            />
      );
    });
  }

  render() {
    if (this.state.loading === true) {
      return (
          <TableSpinnerComponent />
      );
    }
    return (
      <tbody>{this.renderTableRows(this.state.tableData)}</tbody>
    );
  }
}

export default TableClustersBodyContainer;
