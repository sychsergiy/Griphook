import React, { Component } from "react";

import TableClustersBodyContainer from "../containers/tableClustersBody";
import {TableHeaderComponent} from "./tableHeader";


export const TabClustersResourcesComponent = () => {
  return (
     <div className="tab-pane fade show active">
        <div className="table-responsive">
            <table className="table">
                <TableHeaderComponent />
                <TableClustersBodyContainer />
            </table>
        </div>
     </div>
  );
};