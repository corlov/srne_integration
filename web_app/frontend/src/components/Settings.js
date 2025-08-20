import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';
import { logout } from './actions/Auth';
import './styles/Login.css';
import './styles/custom.css';



const Settings = ({width, error, data}) => {
  const renderCardItem = (label, id, value) => (
      <div className="card-title">
        <h6>
          {label}:
          <span id={id} className="badge bg-secondary text-light" style={{ float: 'right', marginTop: '-0.5px', marginLeft: '0.25rem' }}>
            {value}
          </span>
        </h6>
        <hr style={{ marginTop: '-4px', marginBottom: '-4px' }} />
      </div>
  );

  if (data) {
    return (
        <div className="card mb-2 custom-card-light">
            <div className="card-title" style={{ paddingTop: '1rem', marginBottom: '0.5rem', textAlign: 'center' }}>
                <h4><b>Настройки</b></h4>
            </div>
            <div className="card-body" style={{ paddingTop: '0rem', paddingBottom: '0.75rem' }}>
                {renderCardItem("Режим работы светильника", "Mode", data.loadWorkingMode)}
            </div>
        </div>
    );
  } else {
    return (<></>);
  }
};

export default Settings;