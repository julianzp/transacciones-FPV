import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const SuscribirFondo = () => {
  const [form, setForm] = useState({
    clienteId: "1",
    fondoId: "",
    montoInvertido: "",
    notificacion: "sms",
  });

  const [fondos, setFondos] = useState([]);
  const [error, setError] = useState(null);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const fetchFondos = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/fund/all");
        setFondos(response.data);
      } catch (err) {
        setError(err.message);
        setShowErrorModal(true);
      }
    };

    fetchFondos();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar que todos los campos estén llenos
    if (!form.fondoId || !form.montoInvertido || !form.notificacion) {
      setError("Todos los campos son requeridos");
      setShowErrorModal(true);
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/subscription/create",
        form,
      );
      console.log("Response:", response.data);
      setSuccessMessage(
        "¡La suscripción se realizó con éxito! Se le envió la notificación al medio indicado",
      );
      setShowSuccessModal(true);
    } catch (err) {
      console.log(err);
      setError(err.response.data);
      setShowErrorModal(true);
    }
  };

  const closeModal = () => {
    setShowErrorModal(false);
    setShowSuccessModal(false);
    setSuccessMessage("");
    setForm({
      clienteId: "1",
      fondoId: "",
      montoInvertido: "",
      notificacion: "sms",
    });
    window.location.reload();
  };

  return (
    <div className="container">
      <br></br>
      <h2>Suscribirse a un Fondo</h2>

      <div
        className={`modal fade ${showErrorModal ? "show" : ""}`}
        style={{ display: showErrorModal ? "block" : "none" }}
        tabIndex="-1"
        role="dialog"
      >
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Error</h5>
              <button type="button" className="close" onClick={closeModal}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              <p>{error}</p>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={closeModal}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Éxito */}
      <div
        className={`modal fade ${showSuccessModal ? "show" : ""}`}
        style={{ display: showSuccessModal ? "block" : "none" }}
        tabIndex="-1"
        role="dialog"
      >
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Éxito</h5>
              <button type="button" className="close" onClick={closeModal}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body">
              <p>{successMessage}</p>
            </div>
            <div className="modal-footer">
              <button
                type="button"
                className="btn btn-secondary"
                onClick={closeModal}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Fondos</label>
          <select
            className="form-control"
            name="fondoId"
            value={form.fondoId}
            onChange={handleChange}
          >
            <option value="">Selecciona un fondo</option>
            {fondos.map((fondo) => (
              <option key={fondo.FondoId} value={fondo.FondoId}>
                {fondo.Nombre}
              </option>
            ))}
          </select>
        </div>
        <br></br>
        <div className="form-group">
          <label>Monto Invertido</label>
          <input
            type="number"
            className="form-control"
            name="montoInvertido"
            value={form.montoInvertido}
            onChange={handleChange}
          />
        </div>
        <br></br>
        <div className="form-group">
          <label>Notificación</label>
          <select
            className="form-control"
            name="notificacion"
            value={form.notificacion}
            onChange={handleChange}
          >
            <option value="sms">SMS</option>
            <option value="email">Email</option>
          </select>
        </div>
        <br></br>
        <button type="submit" className="btn btn-primary">
          Suscribirse
        </button>
      </form>
    </div>
  );
};

export default SuscribirFondo;
