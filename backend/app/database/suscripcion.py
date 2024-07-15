from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Suscripcion")



def get_subscriptions():

    try:
        response = table.scan(
            Limit=200,
            AttributesToGet=[
                "SuscripcionId",
                "clienteId",
                "fondoId",
                "montoInvertido",
                "fecha",
                "notificacion",
            ],
        )

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def get_subscription(id: str):

    try:
        response = table.query(KeyConditionExpression=Key("SuscripcionId").eq(id))

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def get_subscription_by_fondo(fondoId: str):
    try:
        response = table.query(
            IndexName="FondoIndex", KeyConditionExpression=Key("fondoId").eq(fondoId)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"]["Message"], status_code=500)


def create_subscription(subscripcion: dict):

    try:
        table.put_item(Item=subscripcion)

        return subscripcion

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def delete_subscription(deleteSubscripcion: dict):
    try:
        response = table.delete_item(
            Key={
                "SuscripcionId": deleteSubscripcion["SuscripcionId"],
                "fecha": deleteSubscripcion["fecha"],
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)

def delete_subscription_by_fondoId(deleteSubscripcion: dict):
    try:

        cancelar_fondo =get_subscription_by_fondo(deleteSubscripcion["fondoId"])
        
        response = table.delete_item(
            Key={
                "SuscripcionId": cancelar_fondo[0]["SuscripcionId"],
                "fecha": cancelar_fondo[0]["fecha"]
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)