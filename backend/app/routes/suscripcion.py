from fastapi import APIRouter, Depends, HTTPException
from app.database.suscripcion import get_subscriptions, get_subscription
from app.models.suscripcion import Suscripcion, DeleteSuscripcion
from app.services.subscription_service import subscribe_fund, unsubscribe_fund

router_subscription = APIRouter()


@router_subscription.get("/all")
def get_all_subscriptions():

    return get_subscriptions()


@router_subscription.get("/get/{id}")
def get_subscription_by_id(id: str):

    return get_subscription(id)


@router_subscription.post("/create", response_model=Suscripcion)
def create_new_subscription(suscripcion: Suscripcion):

    return subscribe_fund(suscripcion.dict())


@router_subscription.delete("/delete")
def delete_single_subscription(deleteSuscripcion: DeleteSuscripcion):

    return unsubscribe_fund(deleteSuscripcion.dict())
