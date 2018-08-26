import { connect } from "react-redux";

import DatePicker from "react-datepicker";

import { setTimeFromOption } from "../actions";

const mapStateToProps = state => ({
  selected: state.billing.options.timeFrom
});

const mapDispatchToProps = dispatch => ({
  onChange: date => dispatch(setTimeFromOption(date))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DatePicker);
