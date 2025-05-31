import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card } from "react-bootstrap";
import { ref, onValue } from "firebase/database";
import { db1 } from "./../firebase";
import SensorGauges2 from "./Prediksi2";
import Informasi from "./Informasi";

 
  function SensorGauges() {
    const [pHValue, setPHValue] = useState(0);
    const [temperature, setTemperature] = useState(0);
    const [turbidity, setTurbidity] = useState(0);
    const [prediction, setPredictionCategory] = useState("Loading...");
    const [value, setPredictionValue] = useState(0);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await fetch("http://127.0.0.1:5005/decrypt-data");
          const data = await response.json();
          
          console.log("📡 Data received:", data); // Debugging
    
          if (data.decrypted_data) {
            setPHValue(data.decrypted_data.sensor.PH_AIR);
            setTemperature(data.decrypted_data.sensor.SUHU_AIR);
            setTurbidity(data.decrypted_data.sensor.KEKERUHAN_AIR);

            // Set data prediksi
            setPredictionCategory(data.decrypted_data.prediksi.Kategori);
            setPredictionValue(data.decrypted_data.prediksi.Prediksi);
          } else {
            console.error("❌ Data format unexpected:", data);
          }
        } catch (error) {
          console.error("⚠️ Error fetching decrypted data:", error);
        }
      };
    
      fetchData();
      const interval = setInterval(fetchData, 5000);
    
      return () => clearInterval(interval);
    }, []);
    
  return (
    <div style={{ paddingTop: "120px", textAlign: "center" }}>
      <h4 className="mb-4">Kondisi Kolam 1</h4>
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
        
            {/* <SensorGauges2 /> */}
    
        </Row>

         <Informasi/>
        
      </Container>


      
    </div>
  );
}

export default SensorGauges;
