import React, { useState } from 'react';
import './styles/Login.css';
import axios from 'axios';
import { useDispatch } from 'react-redux';
import { login } from './actions/Auth';



const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const dispatch = useDispatch();

    const loginUser = async () => {
        const response = await axios.post('http://localhost:5000/login', { username, password });
        
        if (response.data.token) {
          dispatch(login({username: username, loginTimestamp: Math.floor(Date.now() / 1000), token: response.data.token}));
        }
        else {
          alert('Failed login!')
        }
    };

    return (
        <div className="container">
            <h1>Авторизация</h1>
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
    );
};

export default Login;
