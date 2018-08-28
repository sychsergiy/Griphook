import React, { Component } from "react";

import {fetchServers, updateServerCPUPrice, updateServerMemoryPrice} from "../fetchHelpers";
import {TableServersRowComponent} from "../components/tableServersRow";
import {getErrorInformation} from "../utils";


class TableServersBodyContainer extends Component {
   constructor(props) {
    super(props);
    this.state = {
      tableData: []
    };
    this.renderTableRows = this.renderTableRows.bind(this);
    this.serverUpdateCPUPrice = this.serverUpdateCPUPrice.bind(this);
    this.serverUpdateMemoryPrice = this.serverUpdateMemoryPrice.bind(this);
  }

  componentDidMount() {
    fetchServers().then(response => {
      if (response.ok) {
        response.json().then(data => {
            this.setState({ tableData: data.servers });
        });
      } else{
        response.json().then(data => {
            // TODO: output !data.error! to modal
            alert(getErrorInformation(data.error));
        });
      }
    });
  }

  serverUpdateCPUPrice(serverId, serverCPUPrice) {
    updateServerCPUPrice(serverId, serverCPUPrice).then(response => {
      if (response.ok) {
          const serverObject = this.state.tableData.find(object => object.id === serverId);
          const objectIndex = this.state.tableData.indexOf(serverObject);

          let tableData = [...this.state.tableData];
          tableData[objectIndex] = { id: serverId, title: serverObject.title, cpu_price: serverCPUPrice, memory_price: serverObject.memory_price};

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

  serverUpdateMemoryPrice(serverId, serverMemoryPrice) {
    updateServerMemoryPrice(serverId, serverMemoryPrice).then(response => {
      if (response.ok) {
          const serverObject = this.state.tableData.find(object => object.id === serverId);
          const objectIndex = this.state.tableData.indexOf(serverObject);

          let tableData = [...this.state.tableData];
          tableData[objectIndex] = { id: serverId, title: serverObject.title, cpu_price: serverObject.cpu_price, memory_price: serverMemoryPrice};

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

  renderTableRows(servers) {
    return servers.map(server => {
        if (server.cpu_price === null) {server.cpu_price = ''}
        if (server.memory_price === null) {server.memory_price = ''}
      return (
          <TableServersRowComponent
            key={server.id}
            serverId={server.id}
            serverTitle={server.title}
            serverCPUPrice={server.cpu_price}
            serverMemoryPrice={server.memory_price}
            serverUpdateCPUPrice={this.serverUpdateCPUPrice}
            serverUpdateMemoryPrice={this.serverUpdateMemoryPrice}
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

export default TableServersBodyContainer;