import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler);

export default function ControllerTempChart({ data }) {
  
  const formatDateToDDMMYY = (dateString) => {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString().slice(-2);
    return `${day}.${month}.${year}`;
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        title: { display: true, text: 'Date', color: '#666' },
        grid: { color: 'rgba(0,0,0,0.1)' }
      },
      y: {
        title: { display: true, text: 'Temperature (°C)', color: '#666' },
        grid: { color: 'rgba(0,0,0,0.1)' },
        beginAtZero: false
      }
    },
    plugins: {
      legend: { 
        display: true,
        position: 'top'
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            return `Temperature: ${context.parsed.y}°C`;
          },
          title: function(context) {
            return new Date(context[0].label).toLocaleDateString();
          }
        }
      }
    },
    maintainAspectRatio: false
  };

  const labelsControllerTemp = data.controller_temperature.map(d => formatDateToDDMMYY(d.x));
  const datasetControllerTemp = {
    labels: labelsControllerTemp,
    datasets: [{
      label: 'Контроллер СП, °C',      
      data: data.controller_temperature.map(d => ({
        x: new Date(d.x),
        y: Number(d.y)
      })),
      borderColor: '#1976d2',
      backgroundColor: 'rgba(25,118,210,0.3)',
      tension: 0.2,
      fill: true,
      pointRadius: 4,
      borderWidth: 2,
      pointBackgroundColor: '#1976d2',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6
    }]
  };


  const labelsBatTemp = data.battery_temperature.map(d => formatDateToDDMMYY(d.x));
  const datasetBatTemp = {
    labels: labelsBatTemp,
    datasets: [{
      label: 'АКБ, температура °C',      
      data: data.battery_temperature.map(d => ({
        x: new Date(d.x),
        y: Number(d.y)
      })),
      borderColor: '#197600',
      backgroundColor: 'rgba(25,218,210,0.3)',
      tension: 0.2,
      fill: true,
      pointRadius: 4,
      borderWidth: 2,
      pointBackgroundColor: '#1976d2',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6
    }]
  };


  const labelsBatV = data.battery_volts.map(d => formatDateToDDMMYY(d.x));
  const datasetBatV = {
    labels: labelsBatV,
    datasets: [{
      label: 'Напряжение на АКБ, V',      
      data: data.battery_volts.map(d => ({
        x: new Date(d.x),
        y: Number(d.y)
      })),
      borderColor: '#ff0000',
      backgroundColor: 'rgba(25,218,210,0.3)',
      tension: 0.2,
      fill: true,
      pointRadius: 4,
      borderWidth: 2,
      pointBackgroundColor: '#1976d2',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6
    }]
  };


  const labelsMaxV = data.maxv.map(d => formatDateToDDMMYY(d.x));
  const datasetMaxV = {
    labels: labelsMaxV,
    datasets: [{
      label: 'MAX на АКБ, V',      
      data: data.maxv.map(d => ({
        x: new Date(d.x),
        y: Number(d.y)
      })),
      borderColor: '#ff0000',
      backgroundColor: 'rgba(25,218,210,0.3)',
      tension: 0.2,
      fill: true,
      pointRadius: 4,
      borderWidth: 2,
      pointBackgroundColor: '#1976d2',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6
    }]
  };


  const labelsMinV = data.minv.map(d => formatDateToDDMMYY(d.x));
  const datasetMinV = {
    labels: labelsMinV,
    datasets: [{
      label: 'Min напряжение за сутки на АКБ, V',
      data: data.minv.map(d => ({
        x: new Date(d.x),
        y: Number(d.y)
      })),
      borderColor: '#ff0000',
      backgroundColor: 'rgba(25,218,210,0.3)',
      tension: 0.2,
      fill: true,
      pointRadius: 4,
      borderWidth: 2,
      pointBackgroundColor: '#1976d2',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverRadius: 6
    }]
  };

  

  return (
    <div style={{ height: 300, width: '100%' }}>
      <Line data={datasetControllerTemp} options={options} />
      <Line data={datasetBatTemp} options={options} />
      <Line data={datasetBatV} options={options} />
      <Line data={datasetMaxV} options={options} />
      <Line data={datasetMinV} options={options} />
    </div>
  );
}
