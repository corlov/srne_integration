import React, { useEffect, useState } from "react";
import { backendEndpoint } from '../../global_consts/Backend'
import Field from './Field'
import { useDispatch } from 'react-redux';
import { useSelector } from 'react-redux';

export default function SettingsTab() {
  const [settings, setSettings] = useState([]);
  const dispatch = useDispatch();
  const authData = useSelector((state) => state.auth);

  const fetchSettings = async () => {
    const res = await fetch(`${backendEndpoint}/get_complex_settings`, {
      method: "GET",
      headers: { Authorization: authData.token },
    });
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