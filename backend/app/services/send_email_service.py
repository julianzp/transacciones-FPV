import smtplib, ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib
from app.models.transaccion import TipoTransaccion

load_dotenv()

email_sender = os.getenv("EMAIL_SENDER")
password = os.getenv("PASSWORD")
subject = "Estado de la Suscripción"


def send_email(email_receiver: str, type_transaction: TipoTransaccion, fondo: str):

    em = EmailMessage()
    context = ssl.create_default_context()
    body = f"Su suscripción al fondo {fondo} está en estado de {type_transaction.value}"

    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    print("¡El email ha sido enviado con éxito!")
