import * as types from "./actionTypes";

import { billingTargetTypes } from "../../common/constants";

import moment from "moment";

const optionsInitialState = {
  timeFrom: moment().subtract(3, "months"),
  timeUntil: moment(),
  targetIDs: [],
  targetType: billingTargetTypes.all
};
export function options(state = optionsInitialState, action) {
  switch (action.type) {
    case types.SET_BILLING_TIME_FROM_OPTION:
      return { ...state, timeFrom: action.date };
    case types.SET_BILLING_TIME_UNTIL_OPTION:
      return { ...state, timeUntil: action.date };
    case types.SET_BILLING_TIME_STEP_OPTION:
      return { ...state, timeStep: action.timeStep };
    case types.SET_BILLING_TARGET_OPTION:
      return {
        ...state,
        targetIDs: [action.targetID],
        targetType: action.targetType
      };
    case types.ADD_GROUP_TO_TARGET_IDS:
      return {
        ...state,
        targetIDs: [...state.targetIDs, action.servicesGroupID]
      };
    case types.REMOVE_GROUP_FROM_TARGET_IDS:
      const indexToRemove = state.targetIDs.indexOf(action.servicesGroupID);
      return {
        ...state,
        targetIDs: [
          ...state.targetIDs.slice(0, indexToRemove),
          ...state.targetIDs.slice(indexToRemove + 1)
        ]
      };
    default:
      return state;
  }
}
