import React from "react";
import "../../assets/styles/SplitPage.css";
import "../../assets/styles/KeyValuePairs.css";



function RightCard({ title, children }) {
  return (
    <section className="card">
      <h3 className="card-title">{title}</h3>
      <div className="card-body">{children}</div>
    </section>
  );
}

export default function ControllerSettingsTab({deviceSettings}) {

    const KeyValuePairs = ({ data, highlightColor = '#e3f2fd' }) => {
        return (
            <div className="key-value-container">
            {Object.entries(data).map(([key, value]) => (
                value ?
                <div key={key} className="key-value-row">
                <span className="key-label">{key}:</span>
                <span 
                    className="value-highlight"
                    style={{ backgroundColor: highlightColor }}
                >
                    {value}
                </span>
                </div> :
                <div key={key} className="key-value-row">
                    <span className="key-label-header">{key}</span>
                </div>
            ))}
            </div>
        );
    };

    
    if (deviceSettings) {    
        console.log(deviceSettings)
        const complexInfoDict = {
            'Общие настройки': '',
            'boostChargingTime': deviceSettings.boostChargingTime,                        
            'boostchargingRecoveryVoltage': deviceSettings.boostchargingRecoveryVoltage,    
            'dischargingLimitVoltage': deviceSettings.dischargingLimitVoltage,    
            'equalizing charging interval': deviceSettings["equalizing charging interval"],
            'equalizingChargingTime': deviceSettings.equalizingChargingTime,    
            'loadWorkingMode': deviceSettings.loadWorkingMode,
            'overDischareTimeDelay': deviceSettings.overDischareTimeDelay,
            'overDischargeRecoveryVoltage': deviceSettings.overDischargeRecoveryVoltage,
            'overDischargeVoltage': deviceSettings.overDischargeVoltage,
            'temperatureCompensationFactor': deviceSettings.temperatureCompensationFactor,
            'underVoltageWarningLevel': deviceSettings.underVoltageWarningLevel,

            'АКБ': '',
            'Тип': deviceSettings.battery.batteryType,
            'boostchargingVoltage': deviceSettings.battery.boostchargingVoltage,
            'equalizingChargingVoltage': deviceSettings.battery.equalizingChargingVoltage,
            'floatingChargingVoltage': deviceSettings.battery.floatingChargingVoltage,
            'nominalBatteryCapacity': deviceSettings.battery.nominalBatteryCapacity,
            'overVoltageThreshold': deviceSettings.battery.overVoltageThreshold,
            'recognizedVoltage': deviceSettings.battery.recognizedVoltage,
            'systemVoltageSetting': deviceSettings.battery.systemVoltageSetting,

            'lightControl': '',
            'lightControlDelay': deviceSettings.lightControl.lightControlDelay,
            'lightControlVoltage': deviceSettings.lightControl.lightControlVoltage,
            'charging method': deviceSettings.lightControl.specialPowerControl["charging method"],
            'eachNightOnFunctionEnabled': deviceSettings.lightControl.specialPowerControl["eachNightOnFunctionEnabled"],
            'noChargingBelowZero': deviceSettings.lightControl.specialPowerControl["noChargingBelowZero"] ? '1' : '0',
            'specialPowerControlFunctionEnabled': deviceSettings.lightControl.specialPowerControl["specialPowerControlFunctionEnabled"] ? '1' : '0'
        };

        return (
        <div className="split-root">       
            <main className="right-col" aria-label="Информация">
            <RightCard title="">            
                <KeyValuePairs data={complexInfoDict}/>
            </RightCard>
            </main>
        </div>
        );
    }
    else {
        return(<></>);
    }
}

