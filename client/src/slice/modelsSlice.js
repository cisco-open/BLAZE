import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'


const initialState = {
    selectedModel:null,
    errors: [],
  };
  
  export const modelSlice = createSlice({
    name: "models",
    initialState,
    reducers: {
      modelSelect: (state,model) => {
          state.selectedModel = model.payload.modelName
      }
    },
    
  });
  export const {modelSelect} = modelSlice.actions
  
  export default modelSlice.reducer;