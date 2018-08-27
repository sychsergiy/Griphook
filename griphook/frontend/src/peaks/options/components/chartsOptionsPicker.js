import React from "react";

import DatePicker from "react-datepicker";

import TimeStepPickerComponent from "./timeStepPicker";

const ChartsOptionsPickerComponent = props => (
  <div className="row">
    <div className="col-12 col-sm-8 offset-sm-2 offset-md-0 col-md-4">
      <div className="form-group">
        <label>Start date</label>
        <div className="input-group">
          <div className="input-group-prepend d-md-none d-lg-flex">
            <span className="input-group-text">
              <i className="far fa-calendar-alt text-primary" />
            </span>
          </div>
          <DatePicker
            selected={props.timeFrom}
            onChange={props.onChangeTimeFrom}
          />
          {/* <input type="datetime-local" className="form-control" id="start-date-input" placeholder=""/> */}
        </div>
      </div>
    </div>

    <div className="col-12 col-sm-8 offset-sm-2 offset-md-0 col-md-4 px-lg-5">
      <div className="form-group">
        <label>Step</label>
        <TimeStepPickerComponent
          currentTimeStep={props.currentTimeStep}
          onTimeStepChange={e => props.onTimeStepChange(e.target.value)}
        />
      </div>
    </div>

    <div className="col-12 col-sm-8 offset-sm-2 offset-md-0 col-md-4">
      <div className="form-group">
        <label>End date</label>
        <div className="input-group">
          <DatePicker
            selected={props.timeUntil}
            onChange={props.onChangeTimeUntil}
          />
          <div className="input-group-append d-md-none d-lg-flex">
            <span className="input-group-text">
              <i className="far fa-calendar-alt text-primary" />
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default ChartsOptionsPickerComponent;
