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
      <div class="card-body">
        <div class="metric-type-filter mb-5 d-flex flex-row">
          <div
            class="custom-control custom-radio mx-3"
            onClick={e => this.setMetricType(metricTypes.cpu)}
          >
            <input
              checked={this.state.metricType === metricTypes.cpu}
              type="radio"
              class="custom-control-input"
              value={metricTypes.cpu}
              onChange={e => {}}
            />
            <label class="custom-control-label">CPU</label>
          </div>
          <div
            class="custom-control custom-radio mx-3"
            onClick={e => this.setMetricType(metricTypes.memory)}
          >
            <input
              type="radio"
              class="custom-control-input"
              checked={this.state.metricType === metricTypes.memory}
              value={metricTypes.memory}
              onChange={e => {}}
            />
            <label class="custom-control-label">Memory</label>
          </div>
        </div>

        <div class="clearfix" />
        <div class="d-flex justify-content-around flex-wrap">
          <div class="row">
            <div class="col-12 mx-auto">
              {/* // TODO: handle charts disappearing */}
              {/* <div class="col-12 col-sm-11 col-md-10 mx-auto"> */}
              <AbsolutePieChartContainer metricType={this.state.metricType} />
            </div>
          </div>

          <div class="row">
            <div class="col-12 mx-auto">
              {/* <div class="col-12 col-sm-11 col-md-10 mx-auto"> */}
              <RelativePieChartContainer metricType={this.state.metricType} />
            </div>
          </div>
        </div>
      </div>
    );
  }
}
export default PieChartsContainer;
