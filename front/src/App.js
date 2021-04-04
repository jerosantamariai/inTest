import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import injectContext from './store/appContext';
import Home from './views/home';
import NotFound from './views/notfound';

const App = props => {
  return (
    <BrowserRouter>
        <div className="row">
          <Switch>
            <Route exact path="/" component={Home} />
            <Route component={NotFound} />
          </Switch>
        </div>
    </BrowserRouter>
  )
}

export default injectContext(App)