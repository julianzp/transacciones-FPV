import os
from dotenv import load_dotenv
from twilio.rest import Client
from app.models.transaccion import TipoTransaccion

load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")


def send_sms(phone_number: str, type_transaction: TipoTransaccion, fondo: str):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Su suscripción al fondo {fondo} está en estado de {type_transaction.value}",
        from_=twilio_number,
        to=phone_number,
    )
    print(message.body)
