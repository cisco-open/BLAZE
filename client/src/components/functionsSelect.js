import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { functionSelect } from "../slice/functionsSlice";
export function FunctionSelect(props) {
    const dispatch = useDispatch();
    const func = useSelector((state) => state.functions.AppFunction);

    let funcChange = (e) => {
        console.log(e.target.value)
        let funcName = e.target.value
        dispatch(functionSelect(funcName))
      };

    const benchmark = props.config["function"]["benchmarking"];
    const custom = props.config["function"]["custom"];
    const comparing = props.config["function"]["comparing"];

    

    return (
        <>
       
        <h5>Please select a function</h5>
        <div>
        <div className="form-check">
            <input
              type="radio"
              className="form-check-input"
              id={"functionOption1"}
              name="functionList"
              value={"custom"}
              onChange={funcChange}
              defaultChecked
            />
            {"Custom"}
            <label
              className="form-check-label"
              htmlFor={"functionOption1"}
            />
          </div>
          { benchmark===true && <div className="form-check">
            <input
              type="radio"
              className="form-check-input"
              id={"functionOption2"}
              name="functionList"
              value={"benchmark"}
              onChange={funcChange}
            />
            {"Benchmark"}
            <label
              className="form-check-label"
              htmlFor={"functionOption2"}
            />
          </div>}
          {comparing===true && <div className="form-check">
            <input
              type="radio"
              className="form-check-input"
              id={"functionOption3"}
              name="functionList"
              value={"comparing"}
              onChange={funcChange}
            />
            {"Comparision"}
            <label
              className="form-check-label"
              htmlFor={"functionOption3"}
            />
          </div>}

        </div>
        
        <hr />
        </>
    )
   

}