import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import LoginPage from './login/index';

import './auth.css';

class AuthPage extends Component {
    render() {
        let matchUrl = this.props.match.url;
        return (
                <Switch>
                    <Route path={`${matchUrl}/login`} component={LoginPage} />
                </Switch>
        );
    }
}

export default AuthPage;