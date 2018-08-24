import { combineReducers } from "redux";

import { hierarchy } from "./reducers/hierarchy";
import { pagination } from "./reducers/pagination";

export const filters = combineReducers({
  hierarchy,
  pagination
});
