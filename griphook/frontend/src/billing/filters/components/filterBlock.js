import React, { Component } from "react";

import { SearchInputComponent } from "./searchInput";

export const FilterBlockComponent = props => {
  const type = props.multiselect ? "checkbox" : "radio";
  return (
    <div className="card my-4 ml-2">
      <div className="text-center filter-group services-filter">
        <h5 className="filter-title">{props.blockTitle}</h5>
        <SearchInputComponent onSearchInputChange={props.onSearchInputChange} />
        <ul className="search-list list-group">
          {props.items.map(item => (
            <li key={item.id} className="list-group-item search-list-item">
              <input
                type={type}
                value={item.id}
                onChange={e => props.onItemClick(parseInt(e.target.value))}
                checked={props.selectedItemIDs.includes(item.id)}
              />
              <label> {item.title} </label>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
