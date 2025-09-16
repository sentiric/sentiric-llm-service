# Multi-stage build
FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev
RUN pip install -U pip poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi --no-root

COPY app ./app
COPY README.md .

# Final stage
FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache curl

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "16010"]