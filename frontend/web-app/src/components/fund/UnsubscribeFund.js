import React, { useState, useEffect } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";

const DesuscribirFondo = () => {
  const [form, setForm] = useState({
    clienteId: "1",
    fondoId: "",
    notificacion: "sms",
  });

  const [fondos, setFondos] = useState([]);
  const [error, setError] = useState(null);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    const fetchFondosSuscritos = async () => {
      try {
        const response = await axios.get(
          "http://3.85.75.66:8000/subscription/all-subscriptions",
        );
        setFondos(response.data);
      } catch (err) {
        setError(err.message);
        setShowErrorModal(true);
      }
    };

    fetchFondosSuscritos();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.fondoId || !form.notificacion) {
      setError("Todos los campos son requeridos");
      setShowErrorModal(true);
      return;
    }

    try {
      const response = await axios.delete(
        "http://3.85.75.66:8000/subscription/delete",
        {
          data: form,
        },
      );
      console.log("Response:", response.data);
      setSuccessMessage(
        "¡Se canceló tu suscripción a este fondo! Se le envió la notificación al medio indicado",
      );
      setShowSuccessModal(true);
    } catch (err) {
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
      notificacion: "sms",
    });
    window.location.reload();
  };

  return (
    <div className="container">
      <br></br>
      <h2>Desuscribirse de un Fondo</h2>

      {/* Modal de Error */}
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

      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Fondos Suscritos</label>
          <select
            className="form-control"
            name="fondoId"
            value={form.fondoId}
            onChange={handleChange}
            disabled={fondos.length === 0}
          >
            <option value="">Selecciona un fondo</option>
            {fondos.map((fondo) => (
              <option key={fondo.FondoId.S} value={fondo.FondoId.S}>
                {fondo.Nombre.S}
              </option>
            ))}
          </select>
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
        <button
          type="submit"
          className="btn btn-danger"
          onClick={handleSubmit}
          disabled={fondos.length === 0}
        >
          Desuscribirse
        </button>
      </form>
    </div>
  );
};

export default DesuscribirFondo;
