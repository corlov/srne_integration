import React from 'react';
import './styles/Login.css';
import './styles/custom.css';



const ContorllerStatus = ({width, error, data}) => {
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
                            <h4><b>Общее</b></h4>
                        </div>
                        <div className="card-body" style={{ paddingTop: '0rem', paddingBottom: '0.75rem' }}>
                            {renderCardItem("Напряжение панели (В)", "PanelVoltage",   error ? '?' : data.panels.volts)}                            
                            {renderCardItem("Напряжение АКБ (В)",    "BatteryVoltage", error ? '?' : data.battery.volts)}
                            {renderCardItem("Уровень заряда АКБ (%)","3", error ? '?' : '?')}
                            {renderCardItem("Ток светильника (А)","4", error ? '?' : data.load.amps)}
                            {renderCardItem("Энергия потребленная светильником за сутки (Вт*ч)","5", error ? '?' : data.load.dailyPower)}
                            {renderCardItem("Состояние зарядка АКБ (вкт/откл)","6", error ? '?' : data.load.stateOfCharge)}
                            {renderCardItem("Состояние светильника (вкт/откл)","7", error ? '?' : String(data.load.state))}
                            {renderCardItem("Температура контроллера (С)","8", error ? '?' : data.controller.temperature)}
                        </div>
                    </div>
            
        );
    }
    else {
        return (<></>);
    }
};

export default ContorllerStatus;