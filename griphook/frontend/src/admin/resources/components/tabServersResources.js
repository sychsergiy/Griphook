import React, { Component } from "react";

import TableServersBodyContainer from "../containers/tableServersBody";
import { TableServerHeaderComponent } from "./tableServerHeader";

export const TabServersResourcesComponent = () => {
  return (
    <div className="tab-pane fade show active">
      <div className="table-responsive">
        <table className="table">
          <TableServerHeaderComponent />
          <TableServersBodyContainer />
        </table>
      </div>
    </div>
  );
};
