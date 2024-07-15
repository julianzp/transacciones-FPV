from decimal import Decimal
from boto3 import resource, client
from os import getenv

# Establecer la conexión con DynamoDB
dynamodb = resource(
    "dynamodb",
    aws_access_key_id=getenv("DB_ACCESS_KEY_ID"),
    aws_secret_access_key=getenv("DB_SECRET_ACCESS_KEY"),
    region_name=getenv("DB_REGION_NAME"),
)

dynamodb_client = client(
    "dynamodb",
    aws_access_key_id=getenv("DB_ACCESS_KEY_ID"),
    aws_secret_access_key=getenv("DB_SECRET_ACCESS_KEY"),
    region_name=getenv("DB_REGION_NAME"),
)

tables = [
    {
        "TableName": "Cliente",
        "AttributeDefinitions": [{"AttributeName": "ClienteId", "AttributeType": "S"}],
        "KeySchema": [{"AttributeName": "ClienteId", "KeyType": "HASH"}],
    },
    {
        "TableName": "Transaccion",
        "AttributeDefinitions": [
            {"AttributeName": "TransaccionId", "AttributeType": "S"},
            {"AttributeName": "fecha", "AttributeType": "S"},
        ],
        "KeySchema": [
            {"AttributeName": "TransaccionId", "KeyType": "HASH"},
            {"AttributeName": "fecha", "KeyType": "RANGE"},
        ],
    },
    {
        "TableName": "Suscripcion",
        "AttributeDefinitions": [
            {"AttributeName": "SuscripcionId", "AttributeType": "S"},
            {"AttributeName": "fecha", "AttributeType": "S"},
            {"AttributeName": "fondoId", "AttributeType": "S"},
        ],
        "KeySchema": [
            {"AttributeName": "SuscripcionId", "KeyType": "HASH"},
            {"AttributeName": "fecha", "KeyType": "RANGE"},
        ],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "FondoIndex",
                "KeySchema": [
                    {"AttributeName": "fondoId", "KeyType": "HASH"},
                    {"AttributeName": "fecha", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            }
        ],
        "BillingMode": "PAY_PER_REQUEST",
    },
    {
        "TableName": "Fondos",
        "AttributeDefinitions": [{"AttributeName": "FondoId", "AttributeType": "S"}],
        "KeySchema": [{"AttributeName": "FondoId", "KeyType": "HASH"}],
    },
]


def create_tables():
    try:
        for table in tables:
            existing_tables = list(dynamodb.tables.all())
            if table["TableName"] not in [t.name for t in existing_tables]:
                dynamodb.create_table(
                    TableName=table["TableName"],
                    KeySchema=table["KeySchema"],
                    AttributeDefinitions=table["AttributeDefinitions"],
                    GlobalSecondaryIndexes=table.get("GlobalSecondaryIndexes", []),
                    BillingMode="PAY_PER_REQUEST",
                )
                print(f'Tabla "{table["TableName"]}" creada exitosamente.')
            else:
                print(
                    f'Tabla "{table["TableName"]}" ya existe, no se creará nuevamente.'
                )
    except Exception as e:
        print(f"Error al crear tablas: {e}")


if __name__ == "__main__":
    create_tables()


def seed_fondos():
    fondos = [
        {
            "FondoId": "1",
            "Nombre": "FPV_EL CLIENTE_RECAUDADORA",
            "categoria": "FPV",
            "monto_minimo": Decimal(75000),
        },
        {
            "FondoId": "2",
            "Nombre": "FPV_EL CLIENTE_ECOPETROL",
            "categoria": "FPV",
            "monto_minimo": Decimal(125000),
        },
        {
            "FondoId": "3",
            "Nombre": "DEUDAPRIVADA",
            "categoria": "FIC",
            "monto_minimo": Decimal(50000),
        },
        {
            "FondoId": "4",
            "Nombre": "FDO-ACCIONES",
            "categoria": "FIC",
            "monto_minimo": Decimal(250000),
        },
        {
            "FondoId": "5",
            "Nombre": "FPV_EL CLIENTE_DINAMICA",
            "categoria": "FPV",
            "monto_minimo": Decimal(100000),
        },
    ]

    table = dynamodb.Table("Fondos")

    for fondo in fondos:
        try:
            table.put_item(Item=fondo)
            print(f'Registro {fondo["FondoId"]} insertado correctamente.')
        except Exception as e:
            print(f"Error al insertar registro {fondo['FondoId']}: {e}")
