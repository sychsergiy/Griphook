import React, { Component } from 'react';
import LoginForm from './login-form';
import { Redirect } from 'react-router-dom';

class LoginPage extends Component {
    render() {
        if (localStorage.getItem('access_token')) {
            return (
                <Redirect to="/settings" />
            );
        }
        return (
            <div className="container">
                <LoginForm />
            </div>
        );
    }
}

export default LoginPage;