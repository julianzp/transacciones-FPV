# transacciones-FPV

## Pasos para Desplegar la aplicación

- Primero, debes autenticarte a AWS ECS en alguna región:
- `aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com`

- Ahora, para desplegar el backend, debes estar en la carpeta 'backend'
 `cd backend`

- Debes tener configurada alguna VPC en AWS, ya que es un parámetro que requiere el despliegue, en específico alguna subnet dentro de VPC

- Crear el stack por medio de cloudFormation:

    aws cloudformation create-stack --stack-name <STACK_NAME> --template-body file://CloudFormation.yaml --capabilities CAPABILITY_NAMED_IAM --parameters 'ParameterKey=SubnetID,ParameterValue=subnet-<SUBNET_ID>'

-Ahora, para desplegar el frontend, debes estar en la carpeta 'frontend'

    cd frontend
- Crea el stack con cloudFormation, puedes usar el mismo comando y cambairle el nombre al stack.