import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout } from '../redux/actions/Auth';
import '../assets/styles/Login.css';
import '../assets/styles/custom.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TabsPage from "./TabsPage";
import { backendEndpoint } from '../global_consts/Backend'

const deviceId = 2


const ComplexStatus = () => {
    const dispatch = useDispatch();
    const authData = useSelector((state) => state.auth);
    const [data, setData] = useState(null);
    const [gpioData, setGpioData] = useState(null);
    const [error, setError] = useState('error');
    const [deviceSettings, setSettings] = useState(null)
    const [deviceSystemInfo, setSystemInfo] = useState(null)
    const [complexInfo, setComplexInfo] = useState(null)

    // FIXME: убрать внешнюю зависимость
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
        const eventSourceUrl = new URL(`${backendEndpoint}/dynamic_data_events/${deviceId}`);
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


    useEffect(() => {
      const eventSourceUrl = new URL(`${backendEndpoint}/gpio_state`);
      eventSourceUrl.searchParams.append('Authorization', authData.token);
      const eventSource = new EventSource(eventSourceUrl.toString());
      
      eventSource.onmessage = (event) => {
          const recvData = JSON.parse(event.data);
          setGpioData(recvData)
      };

      return () => {
          eventSource.close();
      };
  }, [authData.token]);


    const fetchDataFromBackend = async (pointName, callback) => {
      try {
        const response = await axios.get(`${backendEndpoint}/${pointName}`, {headers: { Authorization: authData.token }});
        if (response) {
          callback(response.data)
        }

      } catch (err) {
        console.log(err.message)
        setError(err.message);
      }
    };

    const fetchComplexInfo = async () => {
      fetchDataFromBackend('complex_settings', setComplexInfo)
    };

    const fetchSettingsData = async () => {
      fetchDataFromBackend(`settings?deviceId=${deviceId}`, setSettings)
    };


    const fetchSystemData = async () => {
      fetchDataFromBackend(`system_info?deviceId=${deviceId}`, setSystemInfo)
    };


    useEffect(() => {
      fetchSettingsData();
      fetchSystemData();
      fetchComplexInfo();
    }, []);

    return (
      <>
      {error ? <>Запустите backend!</> :
        <BrowserRouter>
          <Routes>
            <Route path="/*" element={<TabsPage error={error} 
                                                deviceDynamicData={data}
                                                gpioData={gpioData}
                                                deviceSettings={deviceSettings} 
                                                deviceSystemInfo={deviceSystemInfo} 
                                                complexInfo={complexInfo}
                                                logoutUser={logoutUser}/>} />
          </Routes>
        </BrowserRouter>
      }
      </>
    );
};

export default ComplexStatus;




    