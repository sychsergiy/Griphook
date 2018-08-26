import React, { Fragment } from "react";

import ServicesChartContainer from "../containers/ServicesChart";
import ServicesTableContainer from "../containers/ServicesTable";

const CollapsedRowBoxComponent = props => (
  <tr className="collapsable-row">
    <td colSpan="6">
      <div className="collapsed-block">
        {/* // TODO: add loader */}
        {/* <div className="collapse-loader-outer">
          <div className="collapsed-loader mx-auto">
            <div />
            <div />
            <div />
            <div />
          </div>
        </div> */}
        <div className="collapsed-content col-12 col-lg-10 mx-auto">
          <div className="child-services">
            <ServicesTableContainer />
          </div>
        </div>
        <ServicesChartContainer />
      </div>
    </td>
  </tr>
);

const BillingTableRowComponent = props => {
  const iconClass = props.isSelected ? "fa-minus hide" : "fa-plus show";
  const rowClass = props.isSelected ? "table-info" : "";
  return (
    <Fragment>
      <tr className={rowClass}>
        <th scope="row">
          <i
            className={`fas ${iconClass}-collapse-data py-1 px-2`}
            onClick={e =>
              props.onExpandButtonClick(props.item.services_group_id)
            }
          />
        </th>
        <td>{props.item.services_group_title}</td>
        <td>{props.item.team}</td>
        <td>{props.item.project}</td>
        <td>{props.item.cpu_sum}</td>
        <td>{props.item.memory_sum}</td>
      </tr>

      {props.isSelected ? <CollapsedRowBoxComponent /> : null}
    </Fragment>
  );
};

export default BillingTableRowComponent;
