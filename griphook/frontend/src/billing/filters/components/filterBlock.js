import React, { Component } from "react";

import { SearchInputComponent } from "./searchInput";

export const FilterBlockComponentOld = props => {
  const type = props.multiselect ? "checkbox" : "radio";
  return (
    <div className="filter-wrapper col-12 col-sm-6 col-md-12 mx-auto mx-lg-0">
      <div className="card border-primary mt-2 ">
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

import FilterBlockItemComponent from "./filterBlockItem";

{
  /* <i className="fas fa-project-diagram" />; */
  // <i class="fas fa-people-carry mr-2"></i>
  // <i class="fas fa-th-large"></i>
  // <i class="fas fa-server"></i>
  // <i class="fas fa-object-group"></i>
  // <i class="fas fa-cogs"></i>
}

export const FilterBlockComponent = props => {
  return (
    <div className="filter-wrapper col-12 col-sm-6 col-md-12 mx-auto mx-lg-0">
      <div className="card border-primary mt-2 ">
        <h5 className="card-title text-center mt-2">
          <i className={props.blockTitleIconClass} />
          {props.blockTitle}
        </h5>
        <div className="search-input px-3 mb-3">
          <input
            onChange={props.onSearchInputChange}
            type="text"
            className="form-control"
            placeholder="Search..."
          />
        </div>
        {/* <ul className="list-group list-group-flush compact">
          {props.selectedItems.map(item => (
            <FilterBlockItemComponent
              key={item.id}
              item={item}
              isTargetSelected={props.checkIsTargetSelected(item.id)}
              onItemClick={props.onItemClick}
              onIconClick={props.onUnselectFilterItem}
              isItemSelected={true}
            />
          ))}
        </ul> */}

        <ul className="list-group list-group-flush compact mt-3">
          {props.page.items.map(item => (
            <FilterBlockItemComponent
              key={item.id}
              item={item}
              isTargetSelected={props.selectedItemIDs.includes(item.id)}
              onItemClick={props.onItemClick}
              onIconClick={props.onSelectFilterItem}
              isItemSelected={false}
              hideIcon={props.hideIcon}
            />
          ))}
        </ul>

        <div className="pagination mx-auto my-2">
          {props.page.previousPageExists ? (
            <button
              className="btn btn btn-outline-primary btn-sm"
              onClick={() => props.setPageNumber(props.page.pageNumber - 1)}
            >
              Prev
            </button>
          ) : (
            <button className="btn btn btn-outline-primary btn-sm disabled">
              Prev
            </button>
          )}

          <span className="page-number px-4">{props.page.pageNumber}</span>
          {props.page.nextPageExists ? (
            <button
              className="btn btn btn-outline-primary btn-sm"
              onClick={() => props.setPageNumber(props.page.pageNumber + 1)}
            >
              Next
            </button>
          ) : (
            <button className="btn btn btn-outline-primary btn-sm disabled">
              Next
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
