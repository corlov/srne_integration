import React, { useMemo } from 'react';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { NavLink, Routes, Route, Navigate } from "react-router-dom";
import StateTab from "./tabs/StateTab";
import EventsLogTab from "./tabs/EventsLogTab";
import ParamsLogTab from "./tabs/ParamsLogTab";
import SettingsTab from "./tabs/SettingsTab";
import SysInfoTab from "./tabs/SysInfoTab";
import ChartsTab from "./tabs/ChartsTab";
import ControllerSettingsTab from "./tabs/ControllerSettingsTab";
import ControllerInternalHistoryLogTab from "./tabs/ControllerInternalHistoryLog";

import "../assets/styles/tabs.css";


export default function TabsPage({
  error, 
  deviceDynamicData, 
  wifiStatus, 
  gpioData, 
  deviceSettings, 
  deviceSystemInfo, 
  complexInfo, 
  logoutUser, 
  wifiModeHandler,
  keyBtnClick,
  loadControlClick,
  wifiMessage
}) {
    const dispatch = useDispatch();
    const authData = useSelector((state) => state.auth);

    const loginDatetime = useMemo(() => {
        if (!authData.loginTimestamp) return 'Дата не указана';
        
        const timestamp = authData.loginTimestamp;
        const date = timestamp.toString().length === 10 
            ? new Date(timestamp * 1000) 
            : new Date(timestamp);
            
        return date.toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }, [authData.loginTimestamp]);
    
    
    return (
      <div className="tabs-root">
        <header className="app-header">
          <div className="header-left">
            <img src="/rtk_logo.png" alt="Логотип" className="app-logo" />
            <h1 className="app-title">Локальная консоль управления</h1>
          </div>
  
          
          <div className="header-right">
          <div>{wifiMessage}</div>
            Лампа:
            <button className="logout-btn" onClick={() => loadControlClick(1)}>Вкл.</button>
            <button className="logout-btn" onClick={() => loadControlClick(0)}>Откл.</button>
            WiFi:
            <button className="logout-btn" onClick={() => wifiModeHandler(true)}>On</button>
            <button className="logout-btn" onClick={() => wifiModeHandler(false)}>Off</button>
            [Пользователь: <b>{authData.username},</b> дата входа: {loginDatetime}]
            <button className="logout-btn" onClick={logoutUser}>Выход</button>
          </div>
          
        </header>

     
  
        <div className="tabs-container">
          <aside className="tabs-sidebar" aria-label="Меню">
            <nav>
              {authData.username === 'admin' ? (
                <ul>                
                  <li>
                    <NavLink to="state" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Состояние
                    </NavLink>
                  </li>
                  <li>
                    <NavLink to="events" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Журнал событий
                    </NavLink>
                  </li>
                </ul>
              ) : null}

              {authData.username === 'user' ? (
                <ul>
                  <li>
                      <hr/>
                      <b>Автоматизированый Комплекс</b>
                      <hr/>
                  </li>
                  <li>
                    <NavLink to="state" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Состояние
                    </NavLink>
                  </li>
                  <li>
                    <NavLink to="events" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Журнал событий
                    </NavLink>
                  </li>
                  <li>
                    <NavLink to="params" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Журнал параметров
                    </NavLink>
                  </li>
                  <li>
                    <NavLink to="settings" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Настройки
                    </NavLink>
                  </li>

                  <li>
                      <hr/>
                      <b>Контроллер СП</b>
                      <hr/>
                  </li>
                  <li>
                    <NavLink to="system_info" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Системная информация
                    </NavLink>
                  </li>
                  <li>
                    <NavLink to="controller_settings" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Настройки
                    </NavLink>
                  </li>
                  <li>
                    <NavLink to="charts" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Графики параметров работы
                    </NavLink>
                  <li>
                    <NavLink to="internal_log" className={({ isActive }) => (isActive ? "tab active" : "tab")}>
                      Журнал из внутренней памяти
                    </NavLink>
                  </li>
                  </li>
                </ul>
              ) : null}
            </nav>
          </aside>
  
          <main className="tabs-content" role="main">
            <Routes>
              <Route path="/" element={<Navigate to="state" replace />} />
              <Route path="state" element={<StateTab 
                  error={error} 
                  deviceDynamicData={deviceDynamicData}
                  wifiStatus={wifiStatus}
                  gpioData={gpioData} 
                  deviceSettings={deviceSettings} 
                  deviceSystemInfo={deviceSystemInfo} 
                  complexInfo={complexInfo}
                  keyBtnClick={keyBtnClick}
                  />} />
              <Route path="events" element={<EventsLogTab />} />
              <Route path="params" element={<ParamsLogTab />} />
              <Route path="settings" element={<SettingsTab />} />
              <Route path="system_info" element={<SysInfoTab deviceSystemInfo={deviceSystemInfo}/>} />
              <Route path="controller_settings" element={<ControllerSettingsTab deviceSettings={deviceSettings}/>} />
              <Route path="charts" element={<ChartsTab />} />
              <Route path="internal_log" element={<ControllerInternalHistoryLogTab />} />
            </Routes>
          </main>
        </div>
      </div>
    );
  }