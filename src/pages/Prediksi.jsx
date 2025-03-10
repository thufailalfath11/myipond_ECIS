import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card } from "react-bootstrap";
import { ref, onValue } from "firebase/database";
import { db1 } from "./../firebase";
import SensorGauges2 from "./Prediksi2";
import Informasi from "./Informasi";

// Komponen untuk menampilkan data sensor
function SensorGauges() {
  const [pHValue, setPHValue] = useState(0);
  const [temperature, setTemperature] = useState(0);
  const [turbidity, setTurbidity] = useState(0);
  const [prediction, setPredictionCategory] = useState("Loading...");
  const [value, setPredictionValue] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://192.168.1.8:5001/decrypt-data");
        const data = await response.json();
  
        if (data.decrypted) {
          // Set data sensor
          setPHValue(data.decrypted.sensor.PH_AIR);
          setTemperature(data.decrypted.sensor.SUHU_AIR);
          setTurbidity(data.decrypted.sensor.KEKERUHAN_AIR);
  
          // Set data prediksi
          setPredictionCategory(data.decrypted.prediksi.Kategori);
          setPredictionValue(data.decrypted.prediksi.Prediksi);
        } else {
          console.error("❌ Gagal mendapatkan data dekripsi");
        }
      } catch (error) {
        console.error("⚠️ Error fetching decrypted data:", error);
      }
    };
  
    fetchData();
    const interval = setInterval(fetchData, 5000); // Ambil data setiap 5 detik
  
    return () => clearInterval(interval);
  }, []);
  
  return (
    <div style={{ paddingTop: "120px", textAlign: "center" }}>
      <h4 className="mb-4">Kondisi Kolam {value}</h4>
      <p style={{ fontSize: "1.2rem", color: "#555" }}>
        Halo petambak, kondisi kolam kamu{" "}
        <span style={{ fontWeight: "bold", color: "#007bff" }}>{prediction}</span>.
      </p>
      <Container>
        <Row className="justify-content-center">
          {/* pH Sensor */}
          <Col md={4} className="mb-4">
            <Card className="gauge-card text-center p-4 shadow" style={{ borderRadius: "15px" }}>
              <h5 style={{ color: "#333", marginBottom: "20px" }}>Sensor pH</h5>
              <p style={{ fontSize: "1.3em", fontWeight: "bold", color: "#555" }}>
                Nilai pH Kolam Anda adalah: {pHValue}
              </p>
            </Card>
          </Col>

          {/* Temperature Sensor */}
          <Col md={4} className="mb-4">
            <Card className="gauge-card text-center p-4 shadow" style={{ borderRadius: "15px" }}>
              <h5 style={{ color: "#333", marginBottom: "20px" }}>Sensor Suhu</h5>
              <p style={{ fontSize: "1.3em", fontWeight: "bold", color: "#555" }}>
                Suhu Kolam Anda adalah: {temperature} ºC
              </p>
            </Card>
          </Col>

          {/* Turbidity Sensor */}
          <Col md={4} className="mb-4">
            <Card className="gauge-card text-center p-4 shadow" style={{ borderRadius: "15px" }}>
              <h5 style={{ color: "#333", marginBottom: "20px" }}>Sensor Kekeruhan</h5>
              <p style={{ fontSize: "1.3em", fontWeight: "bold", color: "#555" }}>
                Kekeruhan Air adalah: {turbidity} NTU
              </p>
            </Card>
          </Col>
        </Row>
        {/* Komponen Prediksi */}
        <Row>
        
            <SensorGauges2 />
    
        </Row>

         <Informasi/>
        
      </Container>


      
    </div>
  );
}

export default SensorGauges;
