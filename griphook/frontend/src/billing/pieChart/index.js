import React, { Component } from "react";

import { connect } from "react-redux";

import AbsolutePieChartContainer from "./containers/AbsoluteChart";
import RelativePieChartContainer from "./containers/RelativeChart";

import { metricTypes } from "../../common/constants";

class PieChartsContainer extends Component {
  constructor(props) {
    super();
    this.state = {
      metricType: metricTypes.cpu
    };
  }
  setMetricType(value) {
    this.setState({
      metricType: value
    });
  }

  render() {
    return (
      <div className="card-body">
        <div className="metric-type-filter mb-5 d-flex flex-row">
          <div
            className="custom-control custom-radio mx-3"
            onClick={e => this.setMetricType(metricTypes.cpu)}
          >
            <input
              checked={this.state.metricType === metricTypes.cpu}
              type="radio"
              className="custom-control-input"
              value={metricTypes.cpu}
              onChange={e => {}}
            />
            <label className="custom-control-label">CPU</label>
          </div>
          <div
            className="custom-control custom-radio mx-3"
            onClick={e => this.setMetricType(metricTypes.memory)}
          >
            <input
              type="radio"
              className="custom-control-input"
              checked={this.state.metricType === metricTypes.memory}
              value={metricTypes.memory}
              onChange={e => {}}
            />
            <label className="custom-control-label">Memory</label>
          </div>
        </div>

        <div className="clearfix" />
        <div className="d-flex justify-content-around flex-wrap">
            <div className="col-12 col-md-6 col-xl-5 mx-auto">
              <AbsolutePieChartContainer metricType={this.state.metricType} />
            </div>

            <div className="col-12 col-md-6 col-xl-5 mx-auto">
              <RelativePieChartContainer metricType={this.state.metricType} />
            </div>
        </div>
      </div>
    );
  }
}
export default PieChartsContainer;
