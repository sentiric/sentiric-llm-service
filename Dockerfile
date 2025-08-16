# Multi-stage build
FROM python:3.11-alpine AS builder

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

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Ensure the virtual environment's Python is used
ENV PATH="/app/.venv/bin:$PATH"

# Copy the application code
COPY app.py .

# Expose the port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]