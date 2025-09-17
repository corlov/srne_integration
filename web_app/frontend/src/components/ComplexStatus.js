import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout } from '../redux/actions/Auth';
import '../assets/styles/Login.css';
import '../assets/styles/custom.css';
import '../assets/styles/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TabsPage from "./TabsPage";
import { backendEndpoint } from '../global_consts/Backend'

const ComplexStatus = () => {
    const dispatch = useDispatch();
    const authData = useSelector((state) => state.auth);
    const [deviceId, setDeviceId] = useState(authData.deviceId);
    const [data, setData] = useState(null);
    const [gpioData, setGpioData] = useState(null);
    const [wifiStatus, setWifiStatus] = useState(null);
    const [error, setError] = useState('error');
    const [deviceSettings, setSettings] = useState(null)
    const [deviceSystemInfo, setSystemInfo] = useState(null)
    const [complexInfo, setComplexInfo] = useState(null)
    const [wifiMessage, setWifiMessage] = useState('')

    const logoutUser = async () => {
        dispatch(logout());
    };

    const wifiModeHandler = async (mode) => {
      const differenceSeconds = Math.floor((Math.floor(Date.now() / 1000) - authData.loginTimestamp) / 1000);
      if (differenceSeconds <= 5*60) {
        const modeParam = mode ? 'on' : 'off'
        const response = await axios.get(`${backendEndpoint}/wifi_set_state?state=${modeParam}`, 
          {headers: { Authorization: authData.token }});        
        if (response?.data?.message) {
          setWifiMessage(response.data.message)
        }
        else { 
          setWifiMessage(`Передана команда wifi ${mode ? 'вкл' : 'откл'}`)
        }
      }
      else {
        setWifiMessage(`Необходимо перелогинится, время сессии истекло ${differenceSeconds} секунд назад`)
      }
    };

    const keyBtnClick = async (pin_alias) => {
      await axios.get(`${backendEndpoint}/gpio/set_pin?pin=${pin_alias}`, 
        {headers: { Authorization: authData.token }});
    };

    const loadControlClick = async (modeValue) => {
      await axios.get(`${backendEndpoint}/set_controller_load_mode?mode=${modeValue}&device_id=${deviceId}`, 
        {headers: { Authorization: authData.token }});
    };
    

    useEffect(() => {
        const eventSourceUrl = new URL(`${backendEndpoint}/notify/dynamic_data_events/${deviceId}`);
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
        const eventSourceUrl = new URL(`${backendEndpoint}/gpio/state`);
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

    useEffect(() => {
      const eventSourceUrl = new URL(`${backendEndpoint}/notify/complex_events/${deviceId}`);
      eventSourceUrl.searchParams.append('Authorization', authData.token);

      const eventSource = new EventSource(eventSourceUrl.toString());
      
      eventSource.onmessage = (event) => {
          const recvData = JSON.parse(event.data);
          
          console.log(recvData)
          setComplexInfo(recvData.complex_settings)
          setSettings(recvData.device_settings)
          setSystemInfo(recvData.device_system_info)
          setWifiStatus(recvData.wifi)
      };

      return () => {
          eventSource.close();
      };
  }, [authData.token]);

  return (
    <>
    {error ? <>Запустите backend!</> :
      <BrowserRouter>
        <Routes>
          <Route path="/*" element={
            <TabsPage 
              error={error} 
              deviceDynamicData={data}
              wifiStatus={wifiStatus}
              gpioData={gpioData}
              deviceSettings={deviceSettings} 
              deviceSystemInfo={deviceSystemInfo} 
              complexInfo={complexInfo}
              logoutUser={logoutUser}
              wifiModeHandler={wifiModeHandler}
              keyBtnClick={keyBtnClick}
              loadControlClick={loadControlClick}
              wifiMessage={wifiMessage}/>
          } />
        </Routes>
      </BrowserRouter>
    }
    </>
  );
};

export default ComplexStatus;