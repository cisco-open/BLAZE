import React, { Component } from "react";
import { connect } from 'react-redux';
import { simpleAction } from "./actions/simpleAction";
import { decrement,increment } from "./slice/counterSlice";
import "./App.css";
const containerStyle = {
  display: "flex",
};
const buttonStyle = {
  fontSize: "1.5rem",
  width: "40px",
  height: "40px",
};
class Counter extends Component {
  constructor(props) {
    super(props);
    console.log(this.props)
    
  }

  addOne = () => {
    console.log(this.props);
    this.props.increment();
  };
  minusOne = () => {
    console.log(this.props);
    this.props.decrement();
  };
  
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1>{this.props.counterReducer.number}</h1>
          <div style={containerStyle}>
            <button type="button" style={buttonStyle} onClick={this.minusOne}>
              -
            </button>
            <button type="button" style={buttonStyle} onClick={this.addOne}>
              +
            </button>
          </div>
        </header>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
    console.log(state)
    return {
      ...state
    };
  }
const mapDispatchToProps = dispatch => ({
    increment: () => dispatch(increment()),
    decrement: () => dispatch(decrement())
  })
export default connect(mapStateToProps,mapDispatchToProps)(Counter);
