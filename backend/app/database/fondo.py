from .db import dynamodb, dynamodb_client
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


def get_fondos_by_ids(ids: list[str]):

    try:

        if ids == []:
            return []

        response = dynamodb_client.batch_get_item(
            RequestItems={"Fondos": {"Keys": [{"FondoId": {"S": id}} for id in ids]}}
        )
        return response["Responses"]["Fondos"]

    except ClientError as e:
        # Maneja el error y devuelve una respuesta adecuada
        return JSONResponse(content=e.response["Error"]["Message"], status_code=500)
