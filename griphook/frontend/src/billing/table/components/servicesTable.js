import React from "react";

const TableRow = props => (
  <tr>
    <th scope="row">{props.index}</th>
    <td>{props.item.service_title}</td>
    <td>{props.item.cpu / 100}</td>
    <td>{props.item.memory}</td>
  </tr>
);

const ServicesTableComponent = props => (
  <div className="collapsed-content col-12 col-lg-10 mx-auto">
    <table className="table table-sm">
      <caption>Child services</caption>
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Service</th>
          <th scope="col">CPU (core)</th>
          <th scope="col">Memory (GB)</th>
        </tr>
      </thead>
      <tbody>
        {props.services.map((service, index) => (
          <TableRow item={service} key={service.service_id} index={index} />
        ))}
      </tbody>
    </table>
  </div>
);

export default ServicesTableComponent;
