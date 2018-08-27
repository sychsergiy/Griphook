import React, { Component } from "react";

import { SearchInputComponent } from "./controlPanel/searchInput";
import { EditButtonsComponent } from "./controlPanel/editButtons";

export const TableControlPanelComponent = props => {
  return (
    <div className="row mt-5 mr-3">
      <SearchInputComponent onSearchInputChange={props.onSearchInputChange} />
      <EditButtonsComponent showModal={props.showModal} />
    </div>
  );
};
