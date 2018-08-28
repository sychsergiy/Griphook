import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import LoginPage from './login/index';

import './auth.css';

class AuthPage extends Component {
    render() {
        return (
            <div className="login-form">
                <Route path={`${this.props.match.url}/login`} component={LoginPage} />
            </div>

            // <div className="modal" align="center">
            // </div>
        );
    }
}

export default AuthPage;