import React, { useState } from "react";
import "./Principal.css";

const salasData = [
  { id: "cj-102", calidad: "normal", aqi: 30, temp: 20, humedad: 50 },
  { id: "cj-103", calidad: "medio", aqi: 80, temp: 19, humedad: 55 },
  { id: "cj-104", calidad: "alto", aqi: 120, temp: 17, humedad: 45 },
  { id: "cj-105", calidad: "alto", aqi: 180, temp: 16, humedad: 40 },
  { id: "cj-106", calidad: "alto", aqi: 250, temp: 15, humedad: 35 },
  { id: "cj-107", calidad: "alto", aqi: 350, temp: 14, humedad: 30 },
];

const getColor = (calidad) => {
  switch (calidad) {
    case "normal":
      return "sala normal";
    case "medio":
      return "sala medio";
    case "alto":
      return "sala alto";
    default:
      return "sala";
  }
};

const getEstadoCalidad = (aqi) => {
  if (aqi <= 50) return "Buena";
  if (aqi <= 100) return "Moderada";
  if (aqi <= 150) return "Insalubre para grupos sensibles";
  if (aqi <= 200) return "Insalubre";
  if (aqi <= 300) return "Muy insalubre";
  return "Peligrosa";
};

const getColorAQI = (aqi) => {
  if (aqi <= 50) return "verde";
  if (aqi <= 100) return "amarillo";
  if (aqi <= 150) return "naranja";
  if (aqi <= 200) return "rojo";
  if (aqi <= 300) return "morado";
  return "marron";
};

const getDescripcionAQI = (aqi) => {
  if (aqi <= 50) return "Buena";
  if (aqi <= 100) return "Moderada";
  if (aqi <= 150) return "Insalubre para grupos sensibles";
  if (aqi <= 200) return "Insalubre";
  if (aqi <= 300) return "Muy insalubre";
  return "Peligrosa";
};

export default function Principal() {
  const [salaSeleccionada, setSalaSeleccionada] = useState(salasData[0]);

  return (
    <div className="container">
      {/* Panel izquierdo */}
      <div className="panel-izquierdo">
        {salasData.map((sala) => (
          <button
            key={sala.id}
            className={`${getColor(sala.calidad)} ${
              salaSeleccionada.id === sala.id ? "active" : ""
            }`}
            onClick={() => setSalaSeleccionada(sala)}
          >
            {sala.id}
          </button>
        ))}

        {/* Leyenda */}
        <div className="leyenda">
          <div className="caja normal">NORMAL</div>
          <div className="caja medio">MEDIO</div>
          <div className="caja alto">ALTO</div>
        </div>
      </div>

      {/* Panel derecho */}
      <div className="panel-derecho">
        <h2 className="titulo">Sala: {salaSeleccionada.id}</h2>

        <div className={`circulo ${getColorAQI(salaSeleccionada.aqi)}`}>
          <p>Calidad del aire</p>
          <p className="estado">
            {getDescripcionAQI(salaSeleccionada.aqi)}
          </p>
          <p className="valor">{salaSeleccionada.aqi}</p>
          <p>AQI</p>
        </div>

        <table className="tabla">
          <thead>
            <tr>
              <th>Variable ambiental</th>
              <th>Datos</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Calidad del aire</td>
              <td>{salaSeleccionada.aqi}</td>
              <td className={`estado-${getColorAQI(salaSeleccionada.aqi)}`}>{getDescripcionAQI(salaSeleccionada.aqi)}</td>
            </tr>
            <tr>
              <td>Temperatura</td>
              <td>{salaSeleccionada.temp}°C</td>
              <td>{salaSeleccionada.temp < 18 ? "Baja" : salaSeleccionada.temp > 25 ? "Alta" : "Normal"}</td>
            </tr>
            <tr>
              <td>Humedad</td>
              <td>{salaSeleccionada.humedad}%</td>
              <td>{salaSeleccionada.humedad < 30 ? "Baja" : salaSeleccionada.humedad > 70 ? "Alta" : "Normal"}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
