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

    fetch("/train")
      .then(response => response.json())
      .then(data => {
        console.log(data)
        if (data.prediction) {
          console.log(data.prediction)
          console.log("issa success - grabbing prediction")
          this.setState({
            prediction: data.prediction
          })
          // fetch("/predict")
          //   .then(res => res.json())
          //   .then(dat => {
          //     console.log(dat)
          //     this.setState({
          //       prediction: dat.prediction
          //     })
          //   })
          //   .catch(err => {
          //     console.log(err)
          //   })
        }
      })
      .catch(error => {
        console.log(error)
      })

    
  }

  render() {

    return (
      <div className="App">
        <h1>How ya boi die</h1>
        <p>{this.state.death ? this.state.death : "loading"}</p>
        <p>{this.state.prediction ? JSON.stringify(this.state.prediction) : "loading"}</p>

      </div>
    );
  }
}