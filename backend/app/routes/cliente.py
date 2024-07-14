from fastapi import APIRouter, Depends, HTTPException
from app.database.cliente import get_clientes, get_cliente, update_saldo_cliente
from app.models.cliente import UpdateCliente


router_client = APIRouter()


@router_client.get("/all")
def get_all_clients():

    return get_clientes()


@router_client.get("/get/{id}")
def get_client_by_id(id: str):

    return get_cliente(id)


@router_client.patch("/patch")
def update_cliente(updateCliente: UpdateCliente):

    return update_saldo_cliente(updateCliente.dict())
