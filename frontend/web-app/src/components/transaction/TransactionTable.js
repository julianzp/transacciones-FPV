import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

const ListarTabla = () => {
  const [transactions, setTransactions] = useState([]);
  const [setError] = useState(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await axios.get(
          "http://3.85.75.66:8000/transaction/all",
        );
        setTransactions(response.data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchTransactions();
  });

  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 700 }} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Transacción ID</StyledTableCell>
            <StyledTableCell align="right">Cliente ID</StyledTableCell>
            <StyledTableCell align="right">Fondo ID</StyledTableCell>
            <StyledTableCell align="right">Tipo</StyledTableCell>
            <StyledTableCell align="right">Monto</StyledTableCell>
            <StyledTableCell align="right">Notificación</StyledTableCell>
            <StyledTableCell align="right">Fecha</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {transactions.map((transaction) => (
            <StyledTableRow key={transaction.TransaccionId}>
              <StyledTableCell component="th" scope="row">
                {transaction.TransaccionId}
              </StyledTableCell>
              <StyledTableCell align="right">
                {transaction.clienteId}
              </StyledTableCell>
              <StyledTableCell align="right">
                {transaction.fondoId}
              </StyledTableCell>
              <StyledTableCell align="right">
                {transaction.tipo}
              </StyledTableCell>
              <StyledTableCell align="right">
                {transaction.monto}
              </StyledTableCell>
              <StyledTableCell align="right">
                {transaction.notificacion}
              </StyledTableCell>
              <StyledTableCell align="right">
                {transaction.fecha}
              </StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ListarTabla;
