import { configureStore } from '@reduxjs/toolkit'
import rootReducer from './reducers/rootReducer';
import configReducer from './slice/configLoadSlice';
import datasetReducer from './slice/datasetSlice';
import modelReducer from './slice/modelsSlice'
// const store = createStore(
//    rootReducer,
//    applyMiddleware(thunk)
 
// );

const store = configureStore({
   reducer: {
      config: configReducer,
      dataset: datasetReducer,
      models: modelReducer,
   },
})

export default store
