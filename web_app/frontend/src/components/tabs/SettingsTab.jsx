import React, { useEffect, useState } from "react";
import { backendEndpoint } from '../../global_consts/Backend'
import Field from '../Field'



export default function SettingsTab() {
  const [settings, setSettings] = useState([]);

  const fetchSettings = async () => {
    const res = await fetch(`${backendEndpoint}/api/settings`);
    const data = await res.json();
    setSettings(data);
  };

  useEffect(() => { fetchSettings(); }, []);

  return (
    <div>
      <h3>Настройки комплекса</h3>
      {settings.map(s => <Field key={s.id} setting={s} onSave={fetchSettings} />)}
    </div>
  );
}