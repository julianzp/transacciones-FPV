from fastapi import APIRouter, Depends, HTTPException
from app.database.fondo import get_fondos, get_fondo

router_fund = APIRouter()


@router_fund.get("/all")
def get_all_funds():

    return get_fondos()


@router_fund.get("/get/{id}")
def get_fund_by_id(id: str):

    return get_fondo(id)
