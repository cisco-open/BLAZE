import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { modelSelect } from "../slice/modelsSlice";
export function ModelSelect(props) {
    const dispatch = useDispatch();

    let modelChange = (e) => {
        console.log(e.target.value)
        let modelName = e.target.value
        dispatch(modelSelect({"modelName":modelName}))
      };
    let summaryModelList = null
    if ("models_summarization" in props.config){
        summaryModelList = props.config["models_summarization"].map((item, i) => {
        
            return (
              <div className="form-check">
                <input
                  type="radio"
                  className="form-check-input"
                  id={"modelListOption" + String(i)}
                  name="modelList"
                  value={item}
                  onChange={modelChange}
                  defaultChecked
                />
                {item}
                <label
                  className="form-check-label"
                  htmlFor={"modelListOption" + String(i)}
                />
              </div>
            );
          });

    }
    let searchModelList = null
    if ("models_search" in props.config){
      searchModelList = props.config["models_search"].map((item, i) => {
        
        return (
          <div className="form-check">
            <input
              type="radio"
              className="form-check-input"
              id={"modelListOption" + String(i)}
              name="modelList"
              value={item}
              onChange={modelChange}
            />
            {item}
            <label
              className="form-check-label"
              htmlFor={"modelListOption" + String(i)}
            />
          </div>
        );
      });

    }

    return (
        <>
        <a
          href="/"
          className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none"
        >
          <svg className="bi me-2" width={40} height={32}>
            <use xlinkHref="#bootstrap" />
          </svg>
          <span className="fs-4 text-center">{props.config["Title"]}</span>
        </a>
        <hr />
        <h5>Please select a model</h5>
        <div>{summaryModelList}</div>
        <div>{searchModelList}</div>
        <hr />
        </>
    )

}