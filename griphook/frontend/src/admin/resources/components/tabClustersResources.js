import React, { Component } from "react";

import TableClustersBodyContainer from "../containers/tableClustersBody";
import { TableClusterHeaderComponent } from "./tableClusterHeader";

export const TabClustersResourcesComponent = () => {
  return (
    <div className="tab-pane fade show active">
      <div className="table-responsive">
        <table className="table">
          <TableClusterHeaderComponent />
          <TableClustersBodyContainer />
        </table>
      </div>
    </div>
  );
};
