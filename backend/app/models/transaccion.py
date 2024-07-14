from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime


def generate_id():
    return str(uuid4())


def generate_date():
    return str(datetime.now())


class TipoTransaccion(str, Enum):
    apertura = "apertura"
    cancelacion = "cancelacion"


class Notificacion(str, Enum):
    email = "email"
    sms = "sms"


class Transaccion(BaseModel):
    TransaccionId: str = Field(
        default_factory=generate_id, description="Identificador único de la transacción"
    )
    clienteId: str
    fondoId: str
    tipo: TipoTransaccion
    monto: Decimal
    fecha: str = Field(
        default_factory=generate_date, description="Fecha de la transacción"
    )
    notificacion: Notificacion
