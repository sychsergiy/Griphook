import * as types from "./actionTypes";

export const setTimeFromOption = date => ({
  type: types.SET_TIME_FROM_OPTION,
  date
});

export const setTimeUntilOption = date => ({
  type: types.SET_TIME_UNTIL_OPTION,
  date
});

export const setTimeStepOption = timeStep => ({
  type: types.SET_TIME_STEP_OPTION,
  timeStep
});

export const selectPeaksTarget = (targetID, targetType) => ({
  type: types.SELECT_PEAKS_TARGET,
  targetID,
  targetType
});
