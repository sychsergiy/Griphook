import React, { Component } from "react";

import TableServersBodyContainer from "../containers/tableServersBody";
import {TableHeaderComponent} from "./tableHeader";


export const TabServersResourcesComponent = () => {
  return (
    <div className="tab-pane fade show active">
        <div className="table-responsive">
            <table className="table">
                <TableHeaderComponent />
                <TableServersBodyContainer />
            </table>
        </div>
    </div>
  );
};