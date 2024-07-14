from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from app.database.cliente import get_clientes, get_cliente
from app.database.transaccion import create_transaction, get_transactions
from app.models.transaccion import Transaccion

router_transaction = APIRouter()


@router_transaction.get("/all")
def get_all_transactions():

    return get_transactions()


@router_transaction.post("/create", response_model=Transaccion)
def create_new_transaction(transaccion: Transaccion):

    return create_transaction(transaccion.dict())
