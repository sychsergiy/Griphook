import { combineReducers } from "redux";

import { groups } from "./reducers/groups";
import { groupServices } from "./reducers/groupServices";
import { groupChart } from "./reducers/groupChart";

export const table = combineReducers({
  groups,
  groupServices,
  groupChart
});
