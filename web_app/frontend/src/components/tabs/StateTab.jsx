import React from "react";
import "./SplitPage.css";


// const params = Array.from({ length: 15 }, (_, i) => ({
//   name: `Параметр ${i + 1}`,
//   value: `${(Math.random() * 100).toFixed(2)}`,
// }));

function RightCard({ title, children }) {
  return (
    <section className="card">
      <h3 className="card-title">{title}</h3>
      <div className="card-body">{children}</div>
    </section>
  );
}

export default function SplitPage({error, data}) {
    
  if (data) {
    const params = [
        { name: "Напряжение панели (В)", value: data.panels.volts },
    ];
    

    // "Напряжение панели (В)", data.panels.volts)}                            
    //                           {renderCardItem("Напряжение АКБ (В)",    "BatteryVoltage", error ? '?' : data.battery.volts)}
    //                           {renderCardItem("Уровень заряда АКБ (%)","3", error ? '?' : '?')}
    //                           {renderCardItem("Ток светильника (А)","4", error ? '?' : data.load.amps)}
    //                           {renderCardItem("Энергия потребленная светильником за сутки (Вт*ч)","5", error ? '?' : data.load.dailyPower)}
    //                           {renderCardItem("Состояние зарядка АКБ (вкт/откл)","6", error ? '?' : data.load.stateOfCharge)}
    //                           {renderCardItem("Состояние светильника (вкт/откл)","7", error ? '?' : String(data.load.state))}
    //                           {renderCardItem("Температура контроллера (С)","8", error ? '?' : data.controller.temperature)}
    return (
      <div className="split-root">
        <aside className="left-col">
          <div className="card left-card">
            <h3 className="card-title">Текущие значения параметров СП</h3>
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
            </div>
          </div>
        </aside>

        <main className="right-col" aria-label="Информация">
          <RightCard title="Блок 1">
            <p>Краткая информация или показатели.</p>
          </RightCard>

          <RightCard title="Блок 2">
            <p>Другой набор данных.</p>
          </RightCard>
        </main>
      </div>
    );
  }
}