import React from "react";

const TableRow = props => (
  <div className="row">
    <div className="col-md-4 offset-md-2">{props.item.service_title}</div>
    <div className="col-md-3">{props.item.cpu}</div>
    <div className="col-md-3">{props.item.memory}</div>
  </div>
);

const ServicesTableComponent = props => (
  <div id="services-table">
    <div className="container-fluid">
      <div className="row services-table-header">
        <div className="col-md-3 offset-md-3">Service</div>
        <div className="col-md-3">CPU</div>
        <div className="col-md-3">Memory</div>
      </div>
      {props.services.map(service => (
        <TableRow item={service} key={service.service_id} />
      ))}
      <div className="col-md-12">Chart here</div>
    </div>
  </div>
);

export default ServicesTableComponent;
