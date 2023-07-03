import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { datasetSelect } from "../slice/datasetSlice";


export function DatasetSelect(props) {
    const dispatch = useDispatch();

    let datasetChange = (e) => {
        let datasetName = e.target.value
        console.log(datasetName)
        dispatch(datasetSelect({"dataset":datasetName}))
      };
    let datasetList = []  
    if ("datasets" in props.config){
        datasetList = props.config["datasets"].map((item, i) => {
        
            return (
              <div className="form-check">
                <input
                  type="radio"
                  className="form-check-input"
                  id={"datasetListOption" + String(i)}
                  name="datasetList"
                  value={item}
                  onChange={datasetChange}
                />
                {item}
                <label
                  className="form-check-label"
                  htmlFor={"datasetListOption" + String(i)}
                />
              </div>
            );
          });
    }
    return (
        <>
       
        <h5>Please select a dataset</h5>
        <div>{datasetList}</div>
        
        
        </>
    )


}