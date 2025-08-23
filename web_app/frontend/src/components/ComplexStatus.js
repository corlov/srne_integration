import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout } from './actions/Auth';
import ContorllerStatus from './ControllerStatus';
import ConnectionStatus from './ConnectionStatus';
import Settings from './Settings';
import './styles/Login.css';
import './styles/custom.css';

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import TabsPage from "./TabsPage";

const deviceId = 2

const ComplexStatus = () => {
    const dispatch = useDispatch();
    const authData = useSelector((state) => state.auth);
    const [data, setData] = useState(null);
    const [error, setError] = useState('error');
    const [deviceSettings, setSettings] = useState(null)

    useEffect(() => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css';
        document.head.appendChild(link);
    
        // Cleanup function to remove the link when the component unmounts
        return () => {
          document.head.removeChild(link);
        };
      }, []);


    const logoutUser = async () => {
        dispatch(logout());
    };

    // SSE подписка на события об изменении состояния устройства
    useEffect(() => {
        const eventSourceUrl = new URL(`http://192.168.1.193:5011/dynamic_data_events/${deviceId}`);
        eventSourceUrl.searchParams.append('Authorization', authData.token);
        const eventSource = new EventSource(eventSourceUrl.toString());
        
        eventSource.onmessage = (event) => {
            const recvData = JSON.parse(event.data);
            setData(recvData)
            setError('')
        };

        return () => {
            eventSource.close();
        };
    }, [authData.token]);

    const fetchsettingsData = async () => {
      try {
        const response = await axios.get(`http://192.168.1.193:5011/settings?deviceId=${deviceId}`, {headers: { Authorization: authData.token }});
        if (response) {
          setSettings(response.data)
        }

      } catch (err) {
        setError(err.message);
      }
    };

    useEffect(() => {
      fetchsettingsData();
    }, []);

    // return (
    //     <div className="container">
    //         <div>
    //             <div className="button-container">
    //               Пользователь: {authData.username}
    //               <button className="fixed-button" onClick={logoutUser}>Выход</button>
    //             </div>
    //         </div>

    //         {authData.username === 'admin' ? (
    //             <>
    //               <ContorllerStatus width='50%' error={error} data={data}/>
    //               <ConnectionStatus width='49%' error={error} data={data}/>
    //             </>
    //         ) : null}

    //         {authData.username === 'user' ? (
    //             <>
    //               <ContorllerStatus width='50%' error={error} data={data}/>
    //               <Settings width='49%' error={error} data={deviceSettings}/>
    //             </>
    //         ) : null}
    //     </div>
    //  );


     return (
        <BrowserRouter>
        <Routes>
        <Route path="/*" element={<TabsPage error={error} data={data}/>} />
        {/* можно добавить другие маршруты приложения */}
        </Routes>
    </BrowserRouter>
    );

  
};

export default ComplexStatus;




    