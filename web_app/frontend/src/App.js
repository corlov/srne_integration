import React from 'react';
import Login from './components/Login';
import ComplexStatus from './components/ComplexStatus';
import { useSelector } from 'react-redux';


const App = () => {
    const authData = useSelector((state) => state.auth);

    return (
        <div>
            <h1>РТК локальная консоль управления АК</h1>
            <div>
                    {authData.isAuthenticated ? (<ComplexStatus/>) : (<Login/>) }
            </div>
        </div>
    );
};

export default App;
