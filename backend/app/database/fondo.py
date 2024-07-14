from .db import dynamodb
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from boto3.dynamodb.conditions import Key

table = dynamodb.Table("Fondos")


def get_fondos():

    try:
        response = table.scan(
            Limit=200,
            AttributesToGet=["FondoId", "categoria", "monto_minimo", "Nombre"],
        )

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)


def get_fondo(id: str):

    try:
        response = table.query(KeyConditionExpression=Key("FondoId").eq(id))

        return response["Items"]

    except ClientError as e:

        return JSONResponse(content=e.response["error"], status_code=500)
