FROM python:3.11-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.6.1

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./
COPY . .
RUN poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root

FROM base as final

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app .

CMD ["./.venv/bin/python", "main.py"]
