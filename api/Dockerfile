
FROM python:3.12-slim

RUN pip install --no-cache-dir \
    "fastapi" \
    "uvicorn" \
    "httpx" \
    "psycopg[binary]==3.3.6"

WORKDIR /app
COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
