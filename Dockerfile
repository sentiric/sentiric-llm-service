# Multi-stage build
FROM python:3.11-alpine AS builder

# Build argümanlarını build aşamasında kullanılabilir yap
ARG GIT_COMMIT="unknown"
ARG BUILD_DATE="unknown"
ARG SERVICE_VERSION="0.0.0"

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

# Install Poetry
RUN pip install -U pip poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Final stage
FROM python:3.11-alpine

WORKDIR /app

# YENİ: Healthcheck için curl aracını ekliyoruz.
RUN apk add --no-cache curl

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Ensure the virtual environment's Python is used
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY app.py .

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "16010"]