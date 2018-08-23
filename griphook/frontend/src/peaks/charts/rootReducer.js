import { combineReducers } from "redux";

import { averageLoadChart } from "./averageLoad/rootReducer";
import { peaksChart } from "./peaks/rootReducer";

export const charts = combineReducers({
  peaksChart,
  averageLoadChart
});
