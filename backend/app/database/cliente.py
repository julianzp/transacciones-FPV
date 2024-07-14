from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Cliente")


def get_clientes():

    try:
        response = table.scan(
            Limit=200,
            AttributesToGet=[
                "ClienteId",
                "cedula",
                "email",
                "nombre_completo",
                "telefono",
                "saldo",
            ],
        )

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def get_cliente(id: str):

    try:
        response = table.query(KeyConditionExpression=Key("ClienteId").eq(id))

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def update_saldo_cliente(updateCliente: dict):
    try:
        response = table.update_item(
            Key={
                "ClienteId": updateCliente["ClienteId"],
            },
            UpdateExpression="SET saldo = :saldo",
            ExpressionAttributeValues={
                ":saldo": updateCliente["saldo"],
            },
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
