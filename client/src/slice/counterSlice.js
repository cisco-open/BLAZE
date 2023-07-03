import { createSlice } from '@reduxjs/toolkit'


export const counterSlice = createSlice({
    name:'counter',
    initialState: {
        number: 0
    },
    reducers: {
        increment: (state) => {
            state.number +=1
        },
        decrement: (state) => {
            state.number -=1
        },
        reset: (state) => {
            state.number = 0
        }
    }
})

export const {increment,decrement,reset} = counterSlice.actions
export default counterSlice.reducer