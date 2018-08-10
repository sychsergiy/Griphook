import React, { Component } from "react";

import { SearchInputComponent } from "./searchInput";

export const FilterBlockComponent = props => {
  return (
    <div className="card my-4 ml-2">
      <div className="text-center filter-group services-filter">
        <h5 className="filter-title">{props.blockTitle}</h5>
        <ul>
          {props.selectedItems.map(item => (
            <li key={item.id}>
              <input
                type="checkbox"
                value={item.id}
                onChange={props.onFilterToggle}
                checked="checked"
              />
              <label>{item.title}</label>
            </li>
          ))}
        </ul>
        <SearchInputComponent onSearchInputChange={props.onSearchInputChange} />
        <ul className="search-list list-group">
          {props.items.map(item => (
            <li key={item.id} className="list-group-item search-list-item">
              <input
                type="checkbox"
                value={item.id}
                onChange={props.onFilterToggle}
              />
              <label>{item.title}</label>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
