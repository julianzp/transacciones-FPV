from decimal import Decimal
from pydantic import BaseModel


class UpdateCliente(BaseModel):
    ClienteId: str
    saldo: Decimal
