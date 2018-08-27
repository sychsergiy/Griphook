import { combineReducers } from "redux";

import { absoluteChart } from "./reducers/absoluteChart";
import { relativeChart } from "./reducers/relativeChart";

export const pieCharts = combineReducers({
  absoluteChart,
  relativeChart
});
