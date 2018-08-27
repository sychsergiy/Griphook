import { combineReducers } from "redux";

import { chartsOptions } from "./options/rootReducer";
import { filters } from "./filters/rootReducer";
import { charts } from "./charts/rootReducer";

export const peaks = combineReducers({
  filters,
  charts,
  chartsOptions
});
