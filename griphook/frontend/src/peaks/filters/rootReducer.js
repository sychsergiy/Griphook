import { combineReducers } from "redux";

import { hierarchy } from "./reducers/hierarchy";
import { selections } from "./reducers/selections";

export const filters = combineReducers({
  hierarchy,
  selections
});
