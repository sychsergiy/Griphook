import React from "react";

export const TableServerHeaderComponent = () => {
  return (
    <thead>
      <tr>
        <th scope="col">Name</th>
        <th scope="col">Cluster</th>
        <th scope="col">
          CPU Price <i className="fas fa-dollar-sign" />
        </th>
        <th scope="col">
          Memory Price <i className="fas fa-dollar-sign" />
        </th>
      </tr>
    </thead>
  );
};
