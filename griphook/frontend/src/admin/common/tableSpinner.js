import React from "react";
import {Spinner} from "../../common/spinner";


export const TableSpinnerComponent = props => {
  return (
      <tbody>
          <tr>
            <td colSpan="3">
              <Spinner />
            </td>
          </tr>
      </tbody>
  );
};

