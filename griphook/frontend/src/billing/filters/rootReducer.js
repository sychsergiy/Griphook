import { combineReducers } from "redux";

import { hierarchy } from "./reducers/hierarchy";

export const filters = combineReducers({
  hierarchy
});
