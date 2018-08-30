import React, { Fragment } from "react";

import BillingTableRowComponent from "./billingTableRow";

import BillingTablePaginationContainer from "../containers/Pagination";

import { Spinner } from "../../../common/spinner";

const BillingTableComponent = props => {
  let content = null;
  if (props.loading) {
    content = (
      <tr>
        <th colSpan="6">
          <Spinner />
        </th>
      </tr>
    );
  } else if (props.error) {
    content = <div>{props.error.toString()}</div>;
  }

  return (
    <Fragment>
      <div className="table-responsive services-group-table-outer border rounded border-primary">
        <table className="table">
          <thead>
            <tr>
              <th scope="col">
                <span className="px-2">#</span>
              </th>
              <th scope="col">Services group</th>
              <th scope="col">Team</th>
              <th scope="col">Project</th>
              <th scope="col">CPU</th>
              <th scope="col">
                <span className="pr-5 mr-5">Memory</span>
              </th>
            </tr>
          </thead>
          <tbody>
            {content
              ? content
              : props.groups.map(item => (
                  <BillingTableRowComponent
                    key={item.services_group_id}
                    isSelected={
                      props.selectedGroupID === item.services_group_id
                    }
                    item={item}
                    onExpandButtonClick={props.onExpandButtonClick}
                    selectedGroupID={props.selectedGroupID}
                  />
                ))}
          </tbody>
        </table>
      </div>
      <BillingTablePaginationContainer />
    </Fragment>
  );
};

export default BillingTableComponent;
