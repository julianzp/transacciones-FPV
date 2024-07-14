from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Transaccion")


def get_transactions():

    try:
        response = table.scan(
            Limit=200,
            AttributesToGet=[
                "TransaccionId",
                "clienteId",
                "fondoId",
                "tipo",
                "monto",
                "fecha",
                "notificacion",
            ],
        )

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def get_transaction(id: str):

    try:
        response = table.query(KeyConditionExpression=Key("TransaccionId").eq(id))

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def create_transaction(transaccion: dict):

    try:
        table.put_item(Item=transaccion)

        return transaccion

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)
