import React from "react";

import BillingTableRowComponent from "./billingTableRow";

const BillingTableComponent = props => {
  return (
    <div id="billing-table">
      <div className="container-fluid">
        <div className="row billing-table-header">
          <div className="col-md-4">ServicesGroup</div>
          <div className="col-md-3">Project</div>
          <div className="col-md-3">Team</div>
          <div className="col-md-1">CPU</div>
          <div className="col-md-1">Memory</div>
        </div>

        {props.groups.map((item, index) => {
          return (
            <BillingTableRowComponent
              key={item.services_group_id}
              item={item}
              onExpandButtonClick={props.onExpandButtonClick}
              selectedGroupID={props.selectedGroupID}
            />
          );
        })}
      </div>
    </div>
  );
};

export default BillingTableComponent;
