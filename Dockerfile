FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    curl \
    build-essential \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app/backend

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

COPY backend/ /app/backend/

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]