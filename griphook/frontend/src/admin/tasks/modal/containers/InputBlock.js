import React, { Component } from "react";

class InputBlockContainer extends Component {
  constructor(props) {
    super(props);
    this.state = { value: "" };
    this.handleChange = this.handleChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  handleClick(event) {
    this.props.onRowAdd(this.state.value);
    this.setState({ value: "" });
  }

  render() {
    return (
      <div className="input-group mb-3 col-12 col-md-6">
        <input
          type="text"
          value={this.state.value}
          className="form-control"
          placeholder="Enter name ..."
          onChange={this.handleChange}
        />
        <div className="input-group-append">
          <button
            type="submit"
            className="btn btn-outline-primary"
            id="button-addon2"
            onClick={this.handleClick}
          >
            Add object
          </button>
        </div>
      </div>
    );
  }
}

export default InputBlockContainer;
