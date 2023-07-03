import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { listFiles, fileSelect, fileDetails } from "../slice/datasetSlice";

export function FileSelectComponent(props) {
  const dispatch = useDispatch();

  const files = useSelector((state) => {
    return state.dataset.listFiles;
  });
  const selectedDataset = useSelector((state) => state.dataset.selectedDataset);

  React.useEffect(() => {
    console.log(selectedDataset)
    if (selectedDataset !== null){
      dispatch(listFiles(selectedDataset));
    }
  }, [selectedDataset]);

  if (files == null) {
    return <></>;
  }

  const handleOnchange = (e) => {
    console.log(e.target.value)
    let fileclass = e.target.selectedOptions[0].getAttribute('data-fileclass')
    let filename = e.target.value
    dispatch(fileSelect({"filename":filename,"fileclass":fileclass}))
    dispatch(fileDetails({fileclass,filename}))
}

  return (
    <select className="form-select" aria-label="files list" onChange={e => handleOnchange(e)}>
        <option disabled>Please select option below</option>
      {
    
    Object.keys(files).map((value,i)=>{
        return files[value].map((file, index) => {
            return <option value={file} data-fileclass={value}>{file}</option>;
          })
      })
      
      }
      
    
    </select>
  );
}
