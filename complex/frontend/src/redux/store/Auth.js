import { createStore, combineReducers } from 'redux';
import authReducer from '../../redux/reducers/Auth';

const rootReducer = combineReducers({
    auth: authReducer,
});

const store = createStore(rootReducer);

export default store;