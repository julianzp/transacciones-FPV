import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const bull = (
  <Box
    component="span"
    sx={{ display: "inline-block", mx: "2px", transform: "scale(0.8)" }}
  >
    •
  </Box>
);

const CustomerInfoCard = () => {
  const [customer, setCustomer] = React.useState({
    ClienteId: "",
    cedula: "",
    email: "",
    nombre_completo: "",
    saldo: 0,
    telefono: "",
  });
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  const navigate = useNavigate();

  React.useEffect(() => {
    const fetchCustomerInfo = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/client/get/1");
        console.log(response.data[0]);
        setCustomer(response.data[0]);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomerInfo();
  }, []);

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <Card variant="outlined">
        <CardContent>
          <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
            Información de la Cuenta
          </Typography>
          <Typography variant="h5" component="div">
            {customer.nombre_completo}
          </Typography>
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            Cédula: {customer.cedula}
          </Typography>
          <Typography variant="body2">
            <p>Correo Electrónico: {customer.email}</p>
            <p>Teléfono: {customer.telefono}</p>
            <p>Saldo Disponible: ${parseFloat(customer.saldo).toFixed(2)}</p>
          </Typography>
          <Button size="small" onClick={() => navigate("/suscribir-fondo")}>
            Suscribirse a un fondo
          </Button>
          <Button size="small" onClick={() => navigate("/desuscribir-fondo")}>
            Desuscribirse del fondo
          </Button>
          <Button
            size="small"
            onClick={() => navigate("/listar-tabla-transacciones")}
          >
            Ver Tabla de Transacciones
          </Button>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CustomerInfoCard;
