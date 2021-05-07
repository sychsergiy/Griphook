import React from "react";

import InputBoxContainer from "../containers/InputBox";

export const TableServersRowComponent = props => {
  return (
    <tr>
      <td>{props.serverTitle}</td>
      <td>{props.serverClusterTitle}</td>
      <InputBoxContainer
        value={props.serverCPUPrice}
        objectId={props.serverId}
        updateObject={props.serverUpdateCPUPrice}
      />
      <InputBoxContainer
        value={props.serverMemoryPrice}
        objectId={props.serverId}
        updateObject={props.serverUpdateMemoryPrice}
      />
    </tr>
  );
};
