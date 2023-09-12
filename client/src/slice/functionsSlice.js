import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

const initialState = {
    AppFunction:"custom"
    
}

export const functionSlice = createSlice({
    name: "functions",
    initialState,
    reducers: {
      functionSelect: (state,AppFunction) => {
          console.log(AppFunction)
          state.AppFunction = AppFunction.payload
      },
     
    },
   
  });
  export const {functionSelect} = functionSlice.actions
  
  export default functionSlice.reducer;