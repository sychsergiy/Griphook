import React, { Component } from 'react';
import { LOGIN_ENDPOINT } from '../endpoints';

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            password: "",
            isPasswordCorrect: true,
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
                        // if request succeed
                        return response.json()
                    case 401:
                        // if we got unauthorized status code
                        this.setState({ isPasswordCorrect: false })
                        break
                    default:
                        throw Error(response.statusText);
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                localStorage.setItem('access_token', data['access_token'])
            })
            .catch(error => console.log(error));
    };

    handleChange(event) {
        this.setState({ password: event.target.value });
    }

    render() {
        return (
            <form className="login-form" onSubmit={this.handleSubmit}>
                <div className="form-group">
                    <label htmlFor="login-password">Enter password:</label>
                    <input
                        type="password"
                        value={this.state.password}
                        onChange={this.handleChange}
                        id="login-password"
                        className={`form-control is-${this.state.isPasswordCorrect ? 'valid' : 'invalid'}`}
                        placeholder="Password" />
                </div>
                <input className="btn btn-primary" type="submit" value="Login" />
            </form>
        );
    }
}

export default LoginForm;