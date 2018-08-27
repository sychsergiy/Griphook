export const billingTargetTypes = {
  project: "project",
  team: "team",
  cluster: "cluster",
  server: "server",
  group: "services_group",
  all: "all"
};

export const metricTypes = {
  cpu: "user_cpu_percent",
  memory: "vsize"
};

export const INTERVALS = [
  { value: 3600, verbose: "1 Hour" },
  { value: 2 * 3600, verbose: "2 Hours" },
  { value: 24 * 3600, verbose: "1 Day" },
  { value: 2 * 24 * 3600, verbose: "2 Days" },
  { value: 7 * 24 * 3600, verbose: "1 Week" },
  { value: 30 * 24 * 3600, verbose: "1 Month" },
  { value: 3 * 30 * 24 * 3600, verbose: "3 Month" }
];

export const peaksTargetTypes = {
  cluster: "cluster",
  server: "server",
  servicesGroup: "services_group",
  service: "service"
};
