import React from "react";

import ServicesChartContainer from "../containers/ServicesChart";
import ServicesTableContainer from "../containers/ServicesTable";

const BillingTableRowComponent = props => {
  const isSelected = props.selectedGroupID === props.item.services_group_id;
  const icon = isSelected ? "-" : "+";
  return (
    <div className="row">
      <div className="col-md-4">
        <button
          onClick={() => {
            props.onExpandButtonClick(props.item.services_group_id);
          }}
          type="button"
          className="btn btn-sm btn-light"
        >
          {icon}
        </button>
        {props.item.services_group_title}
      </div>
      <div className="col-md-3">{props.item.team}</div>
      <div className="col-md-3">{props.item.project}</div>
      <div className="col-md-1">{props.item.cpu_sum}</div>
      <div className="col-md-1">{props.item.memory_sum}</div>

      {isSelected ? (
        <div className="col-md-12">
          <ServicesTableContainer />
        </div>
      ) : null}
      {isSelected ? (
        <div className="col-md-12">
          <ServicesChartContainer />
        </div>
      ) : null}
    </div>
  );
};

export default BillingTableRowComponent;
