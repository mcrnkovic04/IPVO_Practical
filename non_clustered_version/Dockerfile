FROM python:3.8-slim

WORKDIR /app

COPY . /app

RUN pip install psycopg2-binary faker

CMD ["python", "main.py"]

