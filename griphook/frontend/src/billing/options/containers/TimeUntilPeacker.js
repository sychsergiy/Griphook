import DatePicker from "react-datepicker";
import { connect } from "react-redux";

import { setTimeUntilOption } from "../actions";

const mapStateToProps = state => ({
  selected: state.billing.options.timeUntil
});

const mapDispatchToProps = dispatch => ({
  onChange: date => dispatch(setTimeUntilOption(date))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(DatePicker);
