import React, { useEffect, useState, useRef, useMemo } from 'react';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { NavLink, Routes, Route, Navigate } from "react-router-dom";
import StateTab from "./tabs/StateTab";
import EventsLogTab from "./tabs/EventsLogTab";
import ParamsLogTab from "./tabs/ParamsLogTab";
import SettingsTab from "./tabs/SettingsTab";
import "./tabs/tabs.css";


export default function TabsPage({error, data}) {
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
            [Пользователь: <b>{authData.username},</b> дата входа: {loginDatetime}]
            <button className="logout-btn">Выход</button>
          </div>
        </header>
  
        <div className="tabs-container">
          <aside className="tabs-sidebar" aria-label="Меню">
            <nav>
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
              </ul>
            </nav>
          </aside>
  
          <main className="tabs-content" role="main">
            <Routes>
              <Route path="/" element={<Navigate to="state" replace />} />
              <Route path="state" element={<StateTab error={error} data={data}/>} />
              <Route path="events" element={<EventsLogTab />} />
              <Route path="params" element={<ParamsLogTab />} />
              <Route path="settings" element={<SettingsTab />} />
            </Routes>
          </main>
        </div>
      </div>
    );
  }