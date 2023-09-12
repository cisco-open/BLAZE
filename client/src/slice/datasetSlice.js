import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import {CONSTANTS} from '../CONSTANTS'

const client = axios.create({
  baseURL: CONSTANTS.baseURL,
});

export const listFiles = createAsyncThunk("datasets/files", async (dataset) => {
  return client
    .get("datasets/files", { params: { dataset: dataset } })
    .then((response) => {
      return {[dataset]:response.data.files};
    });
});

export const fileDetails = createAsyncThunk("datasets/files/detail", async ({fileclass,filename}) => {
   
    return client
      .get("datasets/files/detail", { params: { fileclass: fileclass, filename:filename } })
      .then((response) => {
        return response.data
        
      });
  });

const initialState = {
  listFiles: [],
  selectedDataset:null,
  selectedFile:{},
  selectedFileDetails:null,
  errors: [],
};

export const datasetSlice = createSlice({
  name: "datasets",
  initialState,
  reducers: {
    fileSelect: (state,file) => {
        console.log(file)
        state.selectedFile = file.payload
    },
    datasetSelect: (state,dataset) => {
      state.selectedDataset = dataset.payload.dataset

    }
  },
  extraReducers: {
    [listFiles.fulfilled](state, action) {
      state.listFiles = {...action.payload};
    },
    [fileDetails.fulfilled](state, action) {
        state.selectedFileDetails = {...action.payload};
    },
  },
});
export const {fileSelect,datasetSelect} = datasetSlice.actions

export default datasetSlice.reducer;
