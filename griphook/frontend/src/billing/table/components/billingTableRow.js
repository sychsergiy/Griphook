import React, { Fragment } from "react";

import ServicesChartContainer from "../containers/ServicesChart";
import ServicesTableContainer from "../containers/ServicesTable";

const CollapsedRowBoxComponent = props => (
  <tr className="collapsable-row">
    <td colSpan="6">
      <div className="collapsed-block">
        <div className="collapse-loader-outer">
          <div className="collapsed-loader mx-auto">
            <div />
            <div />
            <div />
            <div />
          </div>
        </div>
        <div class="collapsed-content col-12 col-lg-10 mx-auto">
          <div class="child-services">
            <table class="table table-sm">
              <caption>Child services</caption>
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Service</th>
                  <th scope="col">CPU</th>
                  <th scope="col">Memory</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">1</th>
                  <td>Mark</td>
                  <td>10.456</td>
                  <td>1 097 765 Kb.</td>
                </tr>
                <tr>
                  <th scope="row">2</th>
                  <td>Jacob</td>
                  <td>13.533</td>
                  <td>123 053 Kb.</td>
                </tr>
                <tr>
                  <th scope="row">3</th>
                  <td>Some-service</td>
                  <td>0.533</td>
                  <td>539 042 Kb.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        {/*  content here*/}
      </div>
    </td>
  </tr>
);

const BillingTableRowComponent = props => {
  const iconClass = props.isSelected ? "fa-minus hide" : "fa-plus show";
  return (
    <Fragment>
      <tr>
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

{
  /* <div className="row">
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
</div> */
}
