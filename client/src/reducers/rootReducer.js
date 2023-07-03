import { combineReducers } from 'redux';
import countReducer from './simpleReducer';
import counterReducer from '../slice/counterSlice';
import configLoadSlice from '../slice/configLoadSlice';
export default combineReducers({
 countReducer,
 counterReducer
});