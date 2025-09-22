import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login, logout } from '../redux/actions/Auth';
import { backendEndpoint } from '../global_consts/Backend'
import axios from 'axios';
import '../assets/styles/Login.css';

const Login = () => {
    const [username, setUsername] = useState('user');
    const [password, setPassword] = useState('123');
    const [deviceId, setDeviceId] = useState('2'); 

    const dispatch = useDispatch();
    const [error, setError] = useState();

    const loginUser = async () => {
        try {
            const response = await axios.post(`${backendEndpoint}/auth/login`, { username, password });
            setError('')
        
            if (response.data.token) {
                console.log(response.data)
                dispatch(login({
                    username: username, 
                    loginTimestamp: Math.floor(Date.now() / 1000),
                    token: response.data.token,
                    deviceId: deviceId,
                    expiresIn: response.data.exp,
                    role: response.data.role
                }));

                setTimeout(() => {
                    dispatch(logout());
                }, response.data.exp * 1000);
            }
            else {
              setError('Введен неправильный пользователь или пароль')
            }       
        } catch (err) {
            console.log(err)
            setError(`${err.message} (${err.response.data.message})`)
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
                        <label htmlFor="deviceId">ID устройства SmartWatt</label>
                        <select
                            id="deviceId"
                            value={deviceId}
                            onChange={(e) => setDeviceId(e.target.value)}
                        >
                            {[...Array(8)].map((_, i) => {
                            const val = String(i + 1);
                            return (
                                <option key={val} value={val}>
                                {val}
                                </option>
                            );
                            })}
                        </select>
                    </div>

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
