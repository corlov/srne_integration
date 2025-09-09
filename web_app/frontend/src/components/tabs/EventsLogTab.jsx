import React, { useState, useEffect } from 'react';
import { backendEndpoint } from '../../global_consts/Backend'
import '../../assets/styles/Table.css'
import "../../assets/styles/ItemsTable.css"

const EventsLogTab = () => {

  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [limit, setLimit] = useState(10);
  const [eventType, setEventType] = useState("");       // <-- новый
  const [severity, setSeverity] = useState("");         // <-- новый
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const EVENT_TYPE_OPTIONS = [
    { value: "", label: "Все" },
    { value: "EVENT", label: "EVENT" },
    { value: "ERROR", label: "ERROR" },
  ];

  const SEVERITY_OPTIONS = [
    { value: "", label: "Все" },
    { value: "DEBUG", label: "DEBUG" },
    { value: "INFO", label: "INFO" },
    { value: "WARNING", label: "WARNING" },
    { value: "ERROR", label: "ERROR" },
  ];

  const fetchItems = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (startDate) params.append("start_date", startDate);
      if (endDate) params.append("end_date", endDate);
      if (limit !== "" && limit !== null) params.append("limit", limit);
      if (eventType) params.append("event_type", eventType);   // <-- добавить
      if (severity) params.append("severity", severity);       // <-- добавить

      const res = await fetch(`${backendEndpoint}/events_log?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      console.log(data)
      setItems(data.data || []);
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



  const clearLog = async () => {
    setLoading(true);
    setError(null);
    try {      
      const res = await fetch(`${backendEndpoint}/clear_events_log`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      console.log(data)
    } catch (e) {
      setError(e.message || "Ошибка");
    } finally {
      setLoading(false);
    }
  };


  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const onClear = () => {
    setShowConfirmModal(true);
  };

  const handleConfirmClear = () => {
    clearLog();

    setStartDate("");
    setEndDate("");
    setLimit(10);
    setEventType("");
    setSeverity("");
    // остальные set-функции
    setShowConfirmModal(false);
    setItems([]);
  };

  const handleCancelClear = () => {
    setShowConfirmModal(false);
  };

 
  const onExport = () => {
    if (!Array.isArray(items) || items.length === 0) {
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

    <>
      {showConfirmModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1000
        }}>
          <div style={{
            background: 'white',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
            minWidth: '300px'
          }}>
            <h3 style={{ marginTop: 0, color: '#333' }}>Подтверждение</h3>
            <p style={{ margin: '15px 0', color: '#666' }}>Вы уверены, что хотите очистить Журнал?</p>
            <div style={{
              display: 'flex',
              justifyContent: 'flex-end',
              gap: '10px',
              marginTop: '20px'
            }}>
              <button 
                onClick={handleCancelClear}
                style={{
                  padding: '8px 16px',
                  border: 'none',
                  borderRadius: '4px',
                  backgroundColor: '#6c757d',
                  color: 'white',
                  cursor: 'pointer'
                }}
              >
                Отмена
              </button>
              <button 
                onClick={handleConfirmClear}
                style={{
                  padding: '8px 16px',
                  border: 'none',
                  borderRadius: '4px',
                  backgroundColor: '#dc3545',
                  color: 'white',
                  cursor: 'pointer'
                }}
              >
                Очистить
              </button>
            </div>
          </div>
        </div>
      )}
    
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

        <label className="filter-item">
          Тип события:
          <select
            value={eventType}
            onChange={(e) => setEventType(e.target.value)}
            className="filter-input"
          >
            {EVENT_TYPE_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
        </label>

        <label className="filter-item">
          Критичность:
          <select
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="filter-input"
          >
            {SEVERITY_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
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
            Очистить журнал
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
              <th>тип события</th>
              <th>Событие</th>
              <th>Описание</th>
              <th>Устройство</th>
              <th>Критичность</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan="6" className="no-data">Нет данных</td>
              </tr>
            ) : (
              items.map((it, idx) => (
                <tr key={it.created_at ?? idx}>
                  <td>{it.created_at}</td>
                  <td>{it.event_type}</td>
                  <td>{it.event_name}</td>
                  <td>{it.description}</td>
                  <td>{it.device_id}</td>
                  <td>{it.severity}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
    </>
  );
};

export default EventsLogTab;