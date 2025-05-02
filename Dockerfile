FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk update && \
  pip install --upgrade pip

WORKDIR /crypto_bot

# Copy the project into the image
COPY /src /crypto_bot/
COPY pyproject.toml uv.lock /crypto_bot/

# Sync the project
RUN uv sync --no-dev

CMD [".venv/bin/python", "-u", "main.py"]