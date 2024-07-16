import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.transaccion import router_transaction
from app.routes.suscripcion import router_subscription
from app.routes.cliente import router_client
from app.routes.fondo import router_fund
from app.database.db import create_tables, seed_fondos
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_transaction, prefix="/transaction")
app.include_router(router_subscription, prefix="/subscription")
app.include_router(router_client, prefix="/client")
app.include_router(router_fund, prefix="/fund")

create_tables()
seed_fondos()

if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host="0.0.0.0",
        port=8000,
        debug=True,
        env_file=".env",
    )
