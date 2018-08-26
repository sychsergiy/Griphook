import React from "react";

import BillingTableRowComponent from "./billingTableRow";

const BillingTableComponent = props => {
  return (
    <div className="table-responsive services-group-table-outer border rounded border-primary">
      <table className="table">
        <thead>
          <tr>
            <th scope="col">
              <span className="px-2">#</span>
            </th>
            <th scope="col">Services group</th>
            <th scope="col">Project</th>
            <th scope="col">Team</th>
            <th scope="col">CPU</th>
            <th scope="col">
              <span className="pr-5 mr-5">Memory</span>
            </th>
          </tr>
        </thead>
        <tbody>
          {props.groups.map(item => (
            <BillingTableRowComponent
              key={item.services_group_id}
              isSelected={props.selectedGroupID === item.services_group_id}
              item={item}
              onExpandButtonClick={props.onExpandButtonClick}
              selectedGroupID={props.selectedGroupID}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BillingTableComponent;
