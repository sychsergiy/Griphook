import React from "react";

import InputBoxContainer from "../containers/InputBox"


export const TableClustersRowComponent = props => {
  return (
    <tr>
        <td>{props.clusterTitle}</td>
        <InputBoxContainer value={props.clusterCPUPrice} objectId={props.clusterId}  updateObject={props.clusterUpdateCPUPrice} />
        <InputBoxContainer value={props.clusterMemoryPrice} objectId={props.clusterId}  updateObject={props.clusterUpdateMemoryPrice} />
    </tr>
  );
};