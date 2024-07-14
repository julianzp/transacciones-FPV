from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.transaccion import generate_id, generate_date, Notificacion


class Suscripcion(BaseModel):
    SuscripcionId: str = Field(
        default_factory=generate_id, description="Identificador único de la suscripción"
    )
    clienteId: str = Field(..., description="ID del cliente")
    fondoId: str = Field(..., description="ID del fondo")
    montoInvertido: Decimal = Field(
        ..., description="Monto invertido en la suscripción"
    )
    notificacion: Notificacion
    fecha: str = Field(
        default_factory=generate_date, description="Fecha de la suscripción"
    )


class DeleteSuscripcion(BaseModel):
    clienteId: str = Field(..., description="ID del cliente")
    fondoId: str = Field(..., description="ID del fondo")
    notificacion: Notificacion
