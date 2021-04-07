import './App.scss';
import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Nav from './Nav';
import Main from './Main';
import QuickRound from './QuickRound';
import TestMulti from './TestMulti';

class App extends Component {
  constructor() {
    super();
  }

  render() {
    return (
      <Router>
        <div className='container'>
          <Nav />
          <Switch>
            <Route path='/' exact component={Main} />
            <Route path='/quick_round' component={QuickRound} />
            <Route path='/test_multi' component={TestMulti} />
          </Switch>
        </div>
      </Router>
    )
  }
}

export default App;
