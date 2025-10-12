import React, { useEffect, useState } from "react";
import "../../assets/styles/Field.css"
import { backendEndpoint } from '../../global_consts/Backend'
import { useDispatch } from 'react-redux';
import { useSelector } from 'react-redux';


function Field({ setting, onSave }) {
  const dispatch = useDispatch();
  const authData = useSelector((state) => state.auth);
  const [value, setValue] = useState(setting.value);
  const [saving, setSaving] = useState(false);

  useEffect(() => setValue(setting.value), [setting.value]);

  const save = async () => {
    setSaving(true);
    try {
      const body = { value: setting.type === "boolean" ? (value === true || value === "true") : value };
      const res = await fetch(`${backendEndpoint}/update_complex_settings/${setting.id}`, {
        method: "PUT",
        headers: { 
          "Content-Type": "application/json", 
          Authorization: authData.token },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const text = await res.text();
        alert("Error: " + text);
      } else {
        onSave();

        if (setting.param == 'time_source') {
          await fetch(`${backendEndpoint}/apply_time_source`, {
            method: "GET",
            headers: { Authorization: authData.token },
          });
        }
      }
    } finally {
      setSaving(false);
    }
  };

  return (
    
    <>
    {setting.param === 'PIN_OUT_K2_TRAFFICLIGHT' && (
      <div>
        <i><b>GPIO номера разьемов для подключения (изменения вступят в силу только после перезагрузки АК)</b></i>
      </div>
      )}
    <div className="field-grid">
      

      {setting.type === "boolean" ? (
        <div className="field-grid__label-inline" />
      ) : (
        <div className="field-grid__label">{setting.name}</div>
      )}

      <div className="field-grid__inputCell">
        {setting.type === "boolean" ? (
          <label className="field-checkboxLabel">
            <input
              type="checkbox"
              className="field-checkbox"
              checked={value === true || value === "true"}
              onChange={(e) => setValue(e.target.checked)}
            />
            <span className="field-checkboxName">{setting.name}</span>
          </label>
        ) : setting.type === "select" ? (
          <select
            className="field-select"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          >
            {(setting.options || []).map((o) => (
              <option key={o} value={o}>
                {o}
              </option>
            ))}
          </select>
        ) : (
          <input
            className="field-input"
            type="text"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
        )}
      </div>

      <div className="field-grid__btnCell">
        <button
          className={`field-saveBtn ${saving ? "is-saving" : ""}`}
          onClick={save}
          disabled={saving}
          aria-label="Save"
        >
          {saving ? "..." : "✓"}
        </button>
      </div>
    </div>
    </>
  );
}

export default Field;
