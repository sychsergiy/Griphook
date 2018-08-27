import React from "react";

const FilterBlockItemComponent = props => {
  const selectedTargetClass = "list-group-item active-filter active";
  const unSelectedTargetClass = "list-group-item";

  const selectedItemIconClass =
    "fas fa-minus float-right py-1 px-2 remove-filter-rule";
  const unSelectedItemIconClass =
    "fas fa-plus float-right py-1 px-2 add-filter-rule";

  return (
    <li
      className={
        props.isTargetSelected ? selectedTargetClass : unSelectedTargetClass
      }
    >
      <span onClick={() => props.onTargetClick(props.item.id)}>
        {props.item.title}
      </span>

      {!props.hideIcon ? (
        <i
          className={
            props.isItemSelected
              ? selectedItemIconClass
              : unSelectedItemIconClass
          }
          onClick={e => props.onIconClick(props.item.id)}
        />
      ) : null}
    </li>
  );
};

export default FilterBlockItemComponent;
