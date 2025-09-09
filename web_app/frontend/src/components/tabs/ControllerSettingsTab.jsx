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
        //console.log(deviceSettings)
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
            'charging method': deviceSettings.lightControl.specialPowerControl.chargingMethod,
            'eachNightOnFunctionEnabled': deviceSettings.lightControl.specialPowerControl.eachNightOnFunctionEnabled ? 'да' : 'нет',
            'noChargingBelowZero': deviceSettings.lightControl.specialPowerControl.noChargingBelowZero ? 'да' : 'нет',
            'specialPowerControlFunctionEnabled': deviceSettings.lightControl.specialPowerControl.specialPowerControlFunctionEnabled ? 'да' : 'нет'
        };

        function camelCaseToWords(str) {
            // Добавляем пробелы перед заглавными буквами и преобразуем в lowercase
            return str
                .replace(/([A-Z])/g, ' $1')  // Добавляем пробелы перед заглавными буквами
                .replace(/^./, str => str.toUpperCase())  // Первую букву делаем заглавной
                .trim();
        }

        const transformedDict = {};
        for (const [key, value] of Object.entries(complexInfoDict)) {
            // Пропускаем уже отформатированные ключи (с пробелами или русские)
            if (key.includes(' ') || /[а-яА-Я]/.test(key)) {
                transformedDict[key] = value;
            } else {
                transformedDict[camelCaseToWords(key)] = value;
            }
        }


        return (
        <div className="split-root">       
            <main className="right-col" aria-label="Информация">
            <RightCard title="">            
                <KeyValuePairs data={transformedDict}/>
            </RightCard>
            </main>
        </div>
        );
    }
    else {
        return(<></>);
    }
}

