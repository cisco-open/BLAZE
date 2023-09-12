import { configureStore } from '@reduxjs/toolkit'
import rootReducer from './reducers/rootReducer';
import configReducer from './slice/configLoadSlice';
import datasetReducer from './slice/datasetSlice';
import modelReducer from './slice/modelsSlice'
import functionReducer from './slice/functionsSlice'
// const store = createStore(
//    rootReducer,
//    applyMiddleware(thunk)
 
// );

const store = configureStore({
   reducer: {
      config: configReducer,
      dataset: datasetReducer,
      models: modelReducer,
      functions:functionReducer,
   },
})

export default store
