import React from 'react';
import {Route, Switch} from 'react-router-dom';

export const AuthRoutes = () => (
  <Switch>
    <Route exact path="/" component={HomeContainer}/>
    <Route path="/main" component={ProtectedView}/>
    <Route path="/analytics" component={Analytics}/>
    <Route component={NotFound}/>
  </Switch>
);


export const NonAuthRoutes = () => (
  <Switch>
    <Route exact path="/" component={HomeContainer}/>
    <Route path="/login" component={LoginView}/>
    <Route path="/register" component={RegisterView}/>
    <Route path="/home" component={HomeContainer}/>
    <Route component={NotFound}/>
  </Switch>
);

