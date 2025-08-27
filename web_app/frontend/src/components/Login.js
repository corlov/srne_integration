import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from './actions/Auth';
import { backendEndpoint } from '../global_consts/Backend'
import axios from 'axios';
import './styles/Login.css';

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
              setError('Введен неправильный пользователь или пароль')
            }       
        } catch (err) {
            setError(err.message)
        }
    };

    const handleGoHome = () => {
        window.location.href = '/';
    };

    return (
        <> {error ? (
                <div>
                    { (error == 'Network Error') ? (<p>Запустите backend!</p>) : <></>}
                    <p>Текст ошибки: {error}</p>
                    <button className="logout-btn" onClick={handleGoHome}>Назад</button>
                </div>
            ) :
            (
                <div className="container">
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
            )
        }</>
    );
};

export default Login;
