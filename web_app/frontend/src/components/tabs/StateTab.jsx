import React from "react";
import "./SplitPage.css";
import "./styles/KeyValuePairs.css";
import { useMemo } from 'react';


function RightCard({ title, children }) {
  return (
    <section className="card">
      <h3 className="card-title">{title}</h3>
      <div className="card-body">{children}</div>
    </section>
  );
}

export default function StateTab({error, deviceDynamicData, deviceSettings, deviceSystemInfo, complexInfo}) {

  const deviceDynamicDataTime = useMemo(() => {
      if (!deviceDynamicData || !deviceDynamicData.ts) {
          return "Нет данных";
      }

      const timestamp = Math.floor(deviceDynamicData.ts);
      const date = timestamp.toString().length === 10 
          ? new Date(timestamp * 1000) 
          : new Date(timestamp);
          
      return date.toLocaleString('ru-RU', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
      });
  }, [deviceDynamicData?.ts]);

  if (deviceDynamicData && deviceSystemInfo && complexInfo) {    
    
    
  const params = [
    { name: "Напряжение СП (В)", value: deviceDynamicData.panels.volts },
    { name: "Напряжение АКБ (В)", value: deviceDynamicData.battery.volts },
    { name: "Уровень заряда АКБ (%)", value: deviceDynamicData.battery.stateOfCharge },
    { name: "Ток светильника (А)",value: deviceDynamicData.load.amps },
    { name: "Энергия потребленная светильником за сутки (Вт*ч)", value: deviceDynamicData.load.dailyPower },
    { name: "Состояние зарядка АКБ (вкт/откл)", value: (deviceDynamicData.controller.chargingMode == 'OFF' ? 'откл.' : 'вкл.') },
    { name: "Состояние светильника (вкт/откл)", value: (deviceDynamicData.load.state ? 'вкл.' : 'откл.') },
    { name: "Температура контроллера (°С)", value: deviceDynamicData.controller.temperature },
    { name: "Режим работы светильника", value: deviceSettings.loadWorkingMode },
  ];

    
  const additionalParams = [
    { name: "Ошибка в соединении по Modbus", value: (deviceDynamicData.modbusError ? 'есть' : 'нет') },
    { name: "Ток на СП (А)", value: deviceDynamicData.panels.amps },

    { name: "The current day of battery discharging amp-hrs", value: deviceDynamicData.load.dailyAmpHours },
    { name: "Макс.ток разрядки за сегодня (А)", value: deviceDynamicData.load.maxAmps },
    { name: "Макс.мощность разряда за сегодня (Вт)", value: deviceDynamicData.load.maxWatts },
    { name: "The battery of total discharging amp-hrs", value: deviceDynamicData.load.totalAmpHours },
    { name: "The load of Cumulative power consumption", value: deviceDynamicData.load.totalPower },
    { name: "Напряжение на нагрузке (В)", value: deviceDynamicData.load.volts },
    { name: "Ток на нагрузке (А)", value: deviceDynamicData.load.watts },


    { name: "Макс.напряжение на АКБ за сегодня", value: deviceDynamicData.battery.maxVolts },
    { name: "Мин.напряжение на АКБ за сегодня", value: deviceDynamicData.battery.minVolts },
    { name: "Температура АКБ (°С)", value: deviceDynamicData.battery.temperature },

    { name: "Продолжительность работы системы составляет (дней)", value: deviceDynamicData.controller.days },
    { name: "Кол-во полных зарядов АКБ (раз)", value: deviceDynamicData.controller.fullCharges },
    { name: "Кол-во полных разрядок АКБ (раз)", value: deviceDynamicData.controller.overDischarges },

    { name: "Текущая ошибка на контроллере СП", value: deviceDynamicData?.faults?.[0] ?? 'Нет данных' },

    { name: "Ток заряда к АКБ (А)", value: deviceDynamicData.charging.amps },
    { name: "Сколько ушло за сегодня в АКБ (Ач)", value: deviceDynamicData.charging.dailyAmpHours },
    { name: "Power generation of the current day", value: deviceDynamicData.charging.dailyPower },
    { name: "Макс.ток заряда за сегодня", value: deviceDynamicData.charging.maxAmps },
    { name: "Наиб.мощность зарядки за сегодня (Вт)", value: deviceDynamicData.charging.maxWatts },
    { name: "Total chrging amp hours of the battery", value: deviceDynamicData.charging.totalAmpHours },
    { name: "Cumulative power generation", value: deviceDynamicData.charging.totalPower },
    { name: "Мощность зарядки к АКБ (Вт)", value: deviceDynamicData.charging.watts },
  ];

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

  const complexInfoDict = {
    'Версия ПО комплекса':  complexInfo.version,
    'Версия контроллера СП': deviceSystemInfo.hardwareVersion,
    'Серийный номер СП': deviceSystemInfo.serialNumber,
    'Частота записы в журнал параметров работы (сек.)': complexInfo.params_log_period,
    'Коорддинаты местоположения': complexInfo.coordinates,
    'Тип АКБ': complexInfo.battery_type
  };


  // TODO: это заглушки
  const complexState = {
    'WiFi':  'вкл.',
    'Дверь шкафа': 'открыта',
    'Режим работы светильника': 'выкл.',
    'Режим работы светофора': 'режим 1 (500мс, 1Гц)',
    'Ключ К2 (светофор)': 'откл.',
    'Ключ К3 (лампа)': 'вкл.',
    'Ключ К4 (модем)': 'откл.',
  };

  return (
      <div className="split-root">
        <aside className="left-col">
          <div className="card left-card">
            <h3 className="card-title">Текущие значения параметров СП</h3>
            <h3 className="card-title">(данные получены {deviceDynamicDataTime})</h3>
            <div className="card-body">
              <table className="params-table" role="table">
                <tbody>
                  {params.map((p, idx) => (
                    <tr key={idx} className="params-row">
                      <td className="param-name">{p.name}</td>
                      <td className="param-value">{p.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <hr></hr>

              <table className="params-table" role="table">
                <tbody>
                  {additionalParams.map((p, idx) => (
                    <tr key={idx} className="params-row">
                      <td className="param-name">{p.name}</td>
                      <td className="param-value">{p.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </aside>

        <main className="right-col" aria-label="Информация">
          <RightCard title="Система">            
            <KeyValuePairs data={complexInfoDict}/>
          </RightCard>

          <RightCard title="Состояние ">
          <KeyValuePairs data={complexState}/>
          </RightCard>
        </main>
      </div>
    );
  } 
  else {
    return (<div></div>);
  }
}