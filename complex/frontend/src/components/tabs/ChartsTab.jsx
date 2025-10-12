import React, { useEffect, useState } from 'react';
import { backendEndpoint } from '../../global_consts/Backend'
import ControllerTempChart from '../Charts'

export default function ChartsTab() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${backendEndpoint}/charts/get_timeseries?range=30d`)
      .then(res => res.json())
      .then(d => setData(d))
      .catch(console.error);
  }, []);

  if (!('controller_temperature' in data)) {
    return <div>No data</div>;
  }
  return <ControllerTempChart data={data} />;
}