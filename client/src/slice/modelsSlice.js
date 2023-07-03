import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import axios from 'axios'


const initialState = {
    selectedModel:null,
    errors: [],
  };
  
  export const modelSlice = createSlice({
    name: "models",
    initialState,
    reducers: {
      modelSelect: (state,model) => {
          console.log(model)
          state.selectedModel = model.payload.modelName
      }
    },
    
  });
  export const {modelSelect} = modelSlice.actions
  
  export default modelSlice.reducer;