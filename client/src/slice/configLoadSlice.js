import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import axios from 'axios'


const client = axios.create({
    baseURL: "http://localhost:3000/" 
  });



// async function getConfig() {
//     let response = await client.get('config')
//     return {
//         config: response.response
//     }
// }

const initialState = {
    config: null,
    state: "idle",
    errors:[]
}

export const setConfig = createAsyncThunk('config/setConfig', () => {
        return client.get('config')
        .then(response => {
            console.log(response)
            return response.data})
})

export const configSlice = createSlice({
    name:'config',
    initialState,
    reducers:{},
    extraReducers:{
        [setConfig.pending](state){
            state.status = "loading"
        },
        [setConfig.fulfilled](state,action){
            state.config = action.payload.response
            state.state = "success"
        }

    } 
})

export default configSlice.reducer