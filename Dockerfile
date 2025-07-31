# Multi-stage build
FROM python:3.11-alpine AS builder

WORKDIR /app

# Alpine'de gerekli build bağımlılıkları
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

# Poetry'yi kur
RUN pip install -U pip poetry

# Bağımlılık dosyalarını kopyala
COPY pyproject.toml poetry.lock* ./

# Sanal ortam oluştur ve bağımlılıkları kur
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi --no-root

# Son aşama
FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /app/.venv/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/.venv/bin/uvicorn /usr/local/bin/
COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]