import * as types from "./actionTypes";

export const setTimeFromOption = date => ({
  type: types.SET_BILLING_TIME_FROM_OPTION,
  date
});

export const setTimeUntilOption = date => ({
  type: types.SET_BILLING_TIME_UNTIL_OPTION,
  date
});

export const setMetricTypeOption = metricType => ({
  type: types.SET_BILLING_METRIC_TYPE_OPTION,
  metricType
});

export const setTimeStepOption = timeStep => ({
  type: types.SET_BILLING_TIME_STEP_OPTION,
  timeStep
});

export const setTargetOption = (targetID, targetType) => ({
  type: types.SET_BILLING_TARGET_OPTION,
  targetID,
  targetType
});

export const addGroupToTargetIDs = servicesGroupID => ({
  type: types.ADD_GROUP_TO_TARGET_IDS,
  servicesGroupID
});

export const removeGroupFromTargetIDs = servicesGroupID => ({
  type: types.REMOVE_GROUP_FROM_TARGET_IDS,
  servicesGroupID
});
