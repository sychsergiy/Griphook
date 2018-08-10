import { combineReducers } from "redux";
import { filters } from "../filters/reducers";
import { peaks } from "../peaks/rootReducer";

const rootReducer = combineReducers({
  filters,
  peaks
});

export default rootReducer;
