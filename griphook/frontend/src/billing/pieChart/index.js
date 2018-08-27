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
      <div className="col-md-12">
        <button onClick={() => this.setMetricType(metricTypes.cpu)}>CPU</button>
        <button onClick={() => this.setMetricType(metricTypes.memory)}>
          Memory
        </button>

        <div className="row">
          <div className="col-md-6">
            <AbsolutePieChartContainer metricType={this.state.metricType} />
          </div>
          <div className="col-md-6">
            <RelativePieChartContainer metricType={this.state.metricType} />
          </div>
        </div>
      </div>
    );
  }
}
export default PieChartsContainer;
