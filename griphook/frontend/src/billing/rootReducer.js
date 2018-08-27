import { combineReducers } from "redux";

import { filters } from "./filters/rootReducer";
import { options } from "./options/rootReducer";
import { table } from "./table/rootReducer";
import { pieCharts } from "./pieChart/rootReducer";

export const billing = combineReducers({
  filters,
  options,
  table,
  pieCharts
});
