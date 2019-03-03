import React, { Component } from 'react';
import { BrowserRouter, Route } from 'react-router-dom';

import Header from './Header';
import ViewStudents from './ViewStudents';

class App extends Component {
  render() {
    return (
        <div className="app">
            <BrowserRouter>
                <div>
                    <Header />
                    <Route path="/students" exact component={ViewStudents} />
                </div>
            </BrowserRouter>
        </div>
    );
  }
}

export default App;
