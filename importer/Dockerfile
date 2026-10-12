FROM python:3.12-slim

RUN pip install --no-cache-dir "psycopg[binary]==3.3.6"

WORKDIR /app

CMD ["python", "import_documents.py"]
