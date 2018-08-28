import React, { Component } from "react";

import {fetchClusters, updateClusterCPUPrice, updateClusterMemoryPrice} from "../fetchHelpers";
import {getErrorInformation, TableClustersRowComponent} from "../index";


class TableClustersBodyContainer extends Component {
   constructor(props) {
    super(props);
    this.state = {
      tableData: []
    };
    this.renderTableRows = this.renderTableRows.bind(this);
    this.clusterUpdateCPUPrice = this.clusterUpdateCPUPrice.bind(this);
    this.clusterUpdateMemoryPrice = this.clusterUpdateMemoryPrice.bind(this);
  }

  componentDidMount() {
    fetchClusters().then(response => {
      if (response.ok) {
        response.json().then(data => {
            this.setState({ tableData: data.clusters });
        });
      } else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
        });
      }
    });
  }

  clusterUpdateCPUPrice(clusterId, clusterCPUPrice) {
    updateClusterCPUPrice(clusterId, clusterCPUPrice).then(response => {
      if (response.ok) {
          const clusterObject = this.state.tableData.find(object => object.id === clusterId);
          const objectIndex = this.state.tableData.indexOf(clusterObject);

          let tableData = [...this.state.tableData];
          tableData[objectIndex] = { id: clusterId, title: clusterObject.title, cpu_price: clusterCPUPrice, memory_price: clusterObject.memory_price};

          this.setState({tableData: tableData});
      }
      else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
        });
      }
    });
  }

  clusterUpdateMemoryPrice(clusterId, clusterMemoryPrice) {
    updateClusterMemoryPrice(clusterId, clusterMemoryPrice).then(response => {
      if (response.ok) {
          const clusterObject = this.state.tableData.find(object => object.id === clusterId);
          const objectIndex = this.state.tableData.indexOf(clusterObject);

          let tableData = [...this.state.tableData];
          tableData[objectIndex] = { id: clusterId, title: clusterObject.title, cpu_price: clusterObject.cpu_price, memory_price: clusterMemoryPrice};

          this.setState({tableData: tableData});
      }
      else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
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
    return (
      <tbody>{this.renderTableRows(this.state.tableData)}</tbody>
    );
  }
}

export default TableClustersBodyContainer;
