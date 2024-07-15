import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CustomerInfo from "./components/customerBalance/customerBalance";
import SuscribirFondo from "./components/subscribeFund/subscribeFund";
import DesuscribirFondo from "./components/unsubscribeFund/unsubscribeFund";
import ListarTabla from "./components/transactionTable/transactionTable";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CustomerInfo />} />
        <Route path="/suscribir-fondo" element={<SuscribirFondo />} />
        <Route path="/desuscribir-fondo" element={<DesuscribirFondo />} />
        <Route path="/listar-tabla-transacciones" element={<ListarTabla />} />
      </Routes>
    </Router>
  );
}

export default App;