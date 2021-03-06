import React, {Component} from 'react';
import {BrowserRouter as Router, withRouter} from 'react-router-dom';

import './App.css';

export default class App extends Component {
  constructor() {
    super()
    this.state = {
      death: null,
      prediction: null
    }
  }

  componentDidMount() {
    fetch("/api/tester")
      .then(response => response.json())
      .then(data => {
        console.log(data)
        this.setState({
          death: data.death
        })
      })
      .catch(error => {
        console.log(error)
      })

    fetch("/traindeath")
      .then(response => response.json())
      .then(data => {
        console.log(data)
        fetch('/testdeath')
          .then(res => res.json())
          .then(da => {
            console.log(da)
          })
          .catch(er => {
            console.log(er)
          })
      })
      .catch(err => {
        console.log(err)
      })



    
  }

  render() {

    return (
      <div className="App">
        <h1>Deaths and stuff</h1>
        <p>{this.state.death ? this.state.death : "loading"}</p>
        <p>{this.state.prediction ? JSON.stringify(this.state.prediction) : "loading"}</p>

      </div>
    );
  }
}