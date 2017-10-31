import React, {Component} from 'react';
import {BrowserRouter as Router, withRouter} from 'react-router-dom';

import './App.css';

export default class App extends Component {
  constructor() {
    super()
    this.state = {
      fakeData: null
    }
  }

  componentDidMount() {
    fetch("http://localhost:5000/api/tester")
      .then(response => response.json())
      .then(data => {
        console.log(data)
        this.setState({
          fakeData: data
        })
      })
      .catch(error => {
        console.log(error)
      })
  }

  render() {

    return (
      <div className="App">
        <h1>How ya boi die</h1>
        <p>{this.state.fakeData ? this.state.fakeData : "loading"}</p>
      </div>
    );
  }
}