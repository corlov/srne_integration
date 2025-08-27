import React, { useState, useEffect } from 'react';
import { backendEndpoint } from '../../global_consts/Backend'
import '../styles/Table.css'
import "../../assets/styles/ItemsTable.css"

const ParamsLogTab = () => {

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [limit, setLimit] = useState(10);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (startDate) params.append("start_date", startDate);
      if (endDate) params.append("end_date", endDate);
      if (limit !== "" && limit !== null) params.append("limit", limit);

      
      const res = await fetch(`${backendEndpoint}/params_log?${params.toString()}`);
      
      
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      console.log(data)
      setItems(data.data);
    } catch (e) {
      setError(e.message || "Ошибка");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
    // eslint-disable-next-line
  }, []);

  const onApply = () => fetchItems();


  const onClear = () => {
    // setStartDate("");
    // setEndDate("");
    // setLimit(10);
    // setItems([]);
  };

  const onExport = () => {
    console.log(items)
    if (!Array.isArray(items) || items.length === 0) {
      // Можно показать уведомление пользователю вместо silent return
      console.warn("Нет данных для экспорта");
      return;
    }
  
    const headers = Object.keys(items[0] || {});
    if (headers.length === 0) {
      console.warn("Нет заголовков для экспорта");
      return;
    }
  
    const csvRows = [
      headers.join(","),
      ...items.map(row =>
        headers.map(h => {
          const val = row?.[h] ?? "";
          // Экранируем кавычки и оборачиваем в кавычки, если нужно
          return `"${String(val).replace(/"/g, '""')}"`;
        }).join(",")
      )
    ];
  
    const csv = csvRows.join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "export.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };


  return (
    <div className="items-table__wrap">
      <div className="filter-row">
        <label className="filter-item">
          Начальная дата:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="filter-input"
          />
        </label>

        <label className="filter-item">
          Конечная дата:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="filter-input"
          />
        </label>

        <label className="filter-item">
          Количество строк:
          <input
            type="number"
            min="0"
            value={limit}
            onChange={(e) => setLimit(e.target.value === "" ? "" : Number(e.target.value))}
            className="filter-input filter-input--number"
          />
        </label>

        <button className="btn btn--apply" onClick={onApply}>
          Применить
        </button>
      </div>

      <div className="actions-row">
        <div className="actions-left">
          <button className="btn btn--blue btn--fixed" onClick={onExport}>
            Экспорт
          </button>
          <button className="btn btn--blue btn--fixed" onClick={onClear}>
            Очистить
          </button>
        </div>
      </div>

      {loading && <div className="status">Загрузка...</div>}
      {error && <div className="status status--error">{error}</div>}

      <div className="table-scroll">
        <table className="data-table">
          <thead>
            <tr>
              <th>Дата</th>
              <th>U панели, В</th>
              <th>U АКБ, В</th>
              <th>Уровень заряда АКБ, %</th>
              <th>Ток нагрузки, А</th>
              <th>Энергия потребленная, Вт</th>
              <th>Режим заряда</th>
              <th>Нагрузка</th>
              <th>t, °C</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan="4" className="no-data">Нет данных</td>
              </tr>
            ) : (
              items.map((it) => (
                <tr key={it.created_at}>
                  <td>{it.created_at}</td>
                  <td>{it.panel_volts}</td>
                  <td>{it.battery_volts}</td>
                  <td>{it.battery_stateOfCharge}</td>
                  <td>{it.load_amps}</td>
                  <td>{it.load_dailyPower}</td>
                  <td>{it.controller_chargingMode}</td>
                  <td>{it.load_state}</td>
                  <td>{it.controller_temperature}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
        </div>
    </div>
  );

  // return (
  //   <div>
  //     <div style={{ marginBottom: 12 }}>
  //       <label>
  //         Начальная дата:
  //         <input
  //           type="date"
  //           value={startDate}
  //           onChange={(e) => setStartDate(e.target.value)}
  //         />
  //       </label>
  //       <label style={{ marginLeft: 8 }}>
  //         Конечная дата:
  //         <input
  //           type="date"
  //           value={endDate}
  //           onChange={(e) => setEndDate(e.target.value)}
  //         />
  //       </label>
  //       <label style={{ marginLeft: 8 }}>
  //         Количество строк:
  //         <input
  //           type="number"
  //           min="0"
  //           value={limit}
  //           onChange={(e) => setLimit(e.target.value === "" ? "" : Number(e.target.value))}
  //           style={{ width: 80 }}
  //         />
  //       </label>
  //       <button onClick={onApply} style={{ marginLeft: 8 }}>
  //         Применить
  //       </button>

  //       <button onClick={onApply} style={{ marginLeft: 8 }}>
  //         Очистка журнала
  //       </button>

  //       <button onClick={onApply} style={{ marginLeft: 8 }}>
  //         Экспорт
  //       </button>
  //     </div>

  //     {loading && <div>Загрузка...</div>}
  //     {error && <div style={{ color: "red" }}>{error}</div>}

  //     <table border="1" cellPadding="6" cellSpacing="0">
  //       <thead>
  //         <tr>
            // <th>Дата</th>
            // <th>U панели, В</th>
            // <th>U АКБ, В</th>
            // <th>Уровень заряда АКБ, %</th>
            // <th>Ток нагрузки, А</th>
            // <th>Энергия потребленная, Вт</th>
            // <th>Режим заряда</th>
            // <th>Нагрузка</th>
            // <th>t, °C</th>

  //         </tr>
  //       </thead>
  //       <tbody>
  //         {items.length === 0 ? (
  //           <tr>
  //             <td colSpan="4">Нет данных</td>
  //           </tr>
  //         ) : (
          //   items.data.map((it) => (
          //     <tr key={it.created_at}>
          //       <td>{it.created_at}</td>
          //       <td>{it.panel_volts}</td>
          //       <td>{it.battery_volts}</td>
          //       <td>{it.battery_stateOfCharge}</td>
          //       <td>{it.load_amps}</td>
          //       <td>{it.load_dailyPower}</td>
          //       <td>{it.controller_chargingMode}</td>
          //       <td>{it.load_state}</td>
          //       <td>{it.controller_temperature}</td>
          //     </tr>
          //   ))
          // )}
  //       </tbody>
  //     </table>
  //   </div>
  // );
};

export default ParamsLogTab;
