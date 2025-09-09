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

export default function SysInfoTab({deviceSystemInfo}) {

    const KeyValuePairs = ({ data, highlightColor = '#e3f2fd' }) => {
        return (
            <div className="key-value-container">
            {Object.entries(data).map(([key, value]) => (
                <div key={key} className="key-value-row">
                <span className="key-label">{key}:</span>
                <span 
                    className="value-highlight"
                    style={{ backgroundColor: highlightColor }}
                >
                    {value}
                </span>
                </div>
            ))}
            </div>
        );
    };

    if (deviceSystemInfo) {    
        const complexInfoDict = {
            'Max. поддерживаемое напряжение (В)': deviceSystemInfo.maxSupportVoltage,
            'Max. ток заряда (А)': deviceSystemInfo.retedChargingCurrent,
            'Max. ток разряда (А)': deviceSystemInfo.ratedDischargeCurrent,
            'Модель контроллера': deviceSystemInfo.model,
            'Версия ПО': deviceSystemInfo.softwareVersion,
            'Версия железа': deviceSystemInfo.hardwareVersion,
            'Серийный номер': deviceSystemInfo.serialNumber
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

