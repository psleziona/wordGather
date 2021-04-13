import './App.scss';
import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Nav from './Nav';
import Main from './Main';
import QuickRoundContainer from './QuickRoundContainer';
import TestMulti from './TestMulti';
import StatsPage from './StatsPage';
import LoginPage from './LoginPage';

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
            <Route path='/quick_round' component={QuickRoundContainer} />
            <Route path='/test_multi' component={TestMulti} />
            <Route path='/stats' component={StatsPage} />
            <Route path='/login' component={LoginPage} />
          </Switch>
        </div>
      </Router>
    )
  }
}

export default App;
