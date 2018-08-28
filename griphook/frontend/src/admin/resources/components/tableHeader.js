import React from "react";


export const TableHeaderComponent = () => {
  return (
        <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">CPU Price <i className="fas fa-dollar-sign"></i></th>
              <th scope="col">Memory Price <i className="fas fa-dollar-sign"></i></th>
            </tr>
        </thead>
  );
};