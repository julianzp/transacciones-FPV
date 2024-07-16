FROM  python:3.9-slim

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY .env .env

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--env-file", ".env"]
