import { combineReducers } from "redux";

import { hierarchy } from "./reducers/hierarchy";
import { selections } from "./reducers/selections";
import { pagination } from "./reducers/pagination";

export const filters = combineReducers({
  hierarchy,
  selections,
  pagination
});
