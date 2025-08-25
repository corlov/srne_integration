import React, { useState } from 'react';
import './styles/Login.css';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { login } from './actions/Auth';
import { backendEndpoint } from '../global_consts/Backend'


const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const dispatch = useDispatch();
    const [error, setError] = useState();

    const loginUser = async () => {
        try {
            const response = await axios.post(`${backendEndpoint}/login`, { username, password });
            setError('')
        
            if (response.data.token) {
              dispatch(login({username: username, loginTimestamp: Math.floor(Date.now() / 1000), token: response.data.token}));
            }
            else {
              alert('Failed login!')
            }       
        } catch (err) {
            console.log('loginUser:', err.message)
            setError(err)
        }
    };

    return (
        <>
        {error ? <>Запустите backend!</> :
            <div className="container">
                <h2>РТК локальная консоль управления</h2>
                <div className="form-group">
                    <label htmlFor="email">Пользователь</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Пароль</label>
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button onClick={loginUser}>Войти</button>
            </div>
        }
        </>
    );
};

export default Login;
