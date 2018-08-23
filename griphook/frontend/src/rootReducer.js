import { combineReducers } from "redux";

import { peaks } from "./peaks/rootReducer";
import { billing } from "./billing/rootReducer";

const rootReducer = combineReducers({
  peaks,
  billing
});

export default rootReducer;
