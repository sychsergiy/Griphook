import React, { Component } from "react";


class InputBoxContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
        value: this.props.value,
        toolIsActive: false
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleClickAccept = this.handleClickAccept.bind(this);
    this.handleClickCancel = this.handleClickCancel.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value, toolIsActive: true});
  }

  handleClickAccept() {
    this.setState({toolIsActive: false});
    if (this.state.value === "") {
        this.props.updateObject(this.props.objectId, NaN);
    }
    else {
        this.props.updateObject(this.props.objectId, this.state.value);
    }
  }

  handleClickCancel() {
    this.setState({value: this.props.value, toolIsActive: false});
  }

  render() {
    const inputToolClassName = this.state.toolIsActive ? "input-tools" : "input-tools hidden";
    return (
        <td>
            <div className="position-relative">
                <input className="input-price" value={this.state.value} placeholder="Price" type="text" onChange={this.handleChange} />
                    <div className={inputToolClassName}>
                        <i className="fas fa-check accept" onClick={this.handleClickAccept}></i>
                        <i className="fas fa-times ml-2 cancel" onClick={this.handleClickCancel}></i>
                    </div>
            </div>
        </td>
    );
  }
}

export default InputBoxContainer;