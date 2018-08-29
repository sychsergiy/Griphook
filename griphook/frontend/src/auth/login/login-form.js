import React, { Component } from 'react';
import { withRouter } from "react-router-dom";

import { LOGIN_ENDPOINT } from '../endpoints';

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            password: "",
            isPasswordCorrect: true,
            errorMessage: "",
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();

        // get JWT token
        fetch(`/api/${LOGIN_ENDPOINT}`,
            {
                method: "post",
                headers: {
                    'Accept': 'application/json, text/plain',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ password: this.state.password })
            })
            .then(response => {
                switch (response.status) {
                    case 200:
                        // if login succeed reset correct flag
                        this.setState({ isPasswordCorrect: true });
                        return response.json()
                    case 401:
                        // if we got unauthorized status code
                        // return rejected promise with error
                        return response.json().then(data => Promise.reject(data.error));
                    default:
                        throw Error(`[${response.status}] ${response.statusText}`);
                }
            })
            .then(data => {
                // Save access_token to local storage and redirect to settings
                localStorage.setItem('access_token', data.access_token);
                this.props.history.push("/settings");
            })
            .catch(error => {
                this.setState({ isPasswordCorrect: false, errorMessage: error });
            });
    };

    handleChange(event) {
        this.setState({ password: event.target.value });
    }

    render() {
        return (
            <form className="login-form" onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <label htmlFor="login-password">Enter password: </label>
                    <div className="input-group">

                        {/* Password input */}
                        <input
                            type="password"
                            value={this.state.password}
                            onChange={this.handleChange}
                            id="login-password"
                            className={`form-control ${!this.state.isPasswordCorrect ? 'is-invalid' : ''}`}
                            placeholder="Password" />

                        {/* Submit */}
                        <div className="input-group-append">
                            <input
                                className={`btn btn-outline-${this.state.isPasswordCorrect ? 'primary' : 'danger'}`}
                                type="submit"
                                value="Login" />
                        </div>

                    </div>

                    {/* Error message */}
                    {!this.state.isPasswordCorrect && <p className="text-danger">{this.state.errorMessage}</p>}
                </div>
            </form>
        );
    }
}

export default withRouter(LoginForm);