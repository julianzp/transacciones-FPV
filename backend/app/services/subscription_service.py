from app.database.cliente import get_cliente, update_saldo_cliente
from app.database.fondo import get_fondo
from app.database.transaccion import create_transaction
from app.database.suscripcion import (
    create_subscription,
    delete_subscription,
    get_subscription_by_fondo,
)
from app.models.transaccion import (
    generate_id,
    generate_date,
    TipoTransaccion,
    Notificacion,
)
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from app.services.send_email_service import send_email
from app.services.send_sms_service import send_sms


def subscribe_fund(suscripcion: dict):

    try:
        subscripcion_al_fondo = get_subscription_by_fondo(suscripcion["fondoId"])
        fondo = get_fondo(suscripcion["fondoId"])

        if subscripcion_al_fondo:
            return JSONResponse(
                content=f"Ya está suscrito al fondo {fondo[0]['Nombre']}",
                status_code=400,
            )

        if suscripcion["montoInvertido"] < fondo[0]["monto_minimo"]:
            return JSONResponse(
                content=f"El monto invertido debe ser de mínimo {fondo[0]['monto_minimo']} para el fondo {fondo[0]['Nombre']}",
                status_code=400,
            )

        cliente = get_cliente(suscripcion["clienteId"])
        if cliente[0]["saldo"] < fondo[0]["monto_minimo"]:
            return JSONResponse(
                content=f"No tienes saldo para el monto mínimo {fondo[0]['monto_minimo']} del fondo {fondo[0]['Nombre']}",
                status_code=400,
            )

        # Crear transacción
        create_new_transaction(suscripcion, TipoTransaccion.apertura)

        # Actualizar el saldo del cliente
        update_saldo_cliente(
            {
                "ClienteId": suscripcion["clienteId"],
                "saldo": (cliente[0]["saldo"] - suscripcion["montoInvertido"]),
            }
        )

        # Enviar Email o SMS al cliente
        send_email_or_sms(
            suscripcion["notificacion"],
            TipoTransaccion.apertura,
            fondo[0]["Nombre"],
            cliente,
        )

        # Crear suscripción
        suscripcion = {
            "SuscripcionId": generate_id(),
            "clienteId": suscripcion["clienteId"],
            "fondoId": suscripcion["fondoId"],
            "montoInvertido": suscripcion["montoInvertido"],
            "notificacion": suscripcion["notificacion"],
            "fecha": generate_date(),
        }

        return create_subscription(suscripcion)

    except ClientError as e:
        return JSONResponse(content=e.response["error"], status_code=500)


def unsubscribe_fund(suscripcion: dict):

    try:
        suscripcion_done = get_subscription_by_fondo(suscripcion["fondoId"])

        if not suscripcion_done:
            return JSONResponse(
                content="No está suscrito a este fondo", status_code=400
            )

        # Crear transacción
        create_new_transaction(suscripcion_done[0], TipoTransaccion.cancelacion)

        # Actualizar el saldo del cliente
        cliente = get_cliente(suscripcion_done[0]["clienteId"])
        update_saldo_cliente(
            {
                "ClienteId": suscripcion_done[0]["clienteId"],
                "saldo": (cliente[0]["saldo"] + suscripcion_done[0]["montoInvertido"]),
            }
        )

        # Enviar Email o SMS al cliente
        fondo = get_fondo(suscripcion_done[0]["fondoId"])
        send_email_or_sms(
            suscripcion["notificacion"],
            TipoTransaccion.cancelacion,
            fondo[0]["Nombre"],
            cliente,
        )

        # Eliminar la suscripción al fondo
        return delete_subscription(
            {
                "SuscripcionId": suscripcion_done[0]["SuscripcionId"],
                "fecha": suscripcion_done[0]["fecha"],
            }
        )

    except ClientError as e:
        return JSONResponse(content=e.response["error"], status_code=500)


def create_new_transaction(suscripcion, tipo: TipoTransaccion):
    transaccion = {
        "TransaccionId": generate_id(),
        "clienteId": suscripcion["clienteId"],
        "fondoId": suscripcion["fondoId"],
        "tipo": tipo,
        "monto": suscripcion["montoInvertido"],
        "fecha": generate_date(),
        "notificacion": suscripcion["notificacion"],
    }

    create_transaction(transaccion)


def send_email_or_sms(
    tipo_notificacion: Notificacion,
    tipo_transaccion: TipoTransaccion,
    nombre_fondo: str,
    cliente,
):
    if tipo_notificacion == Notificacion.email:
        send_email(cliente[0]["email"], tipo_transaccion, nombre_fondo)
    elif tipo_notificacion == Notificacion.sms:
        send_sms(cliente[0]["telefono"], tipo_transaccion, nombre_fondo)
