FROM python:3.14-slim

# Copy the uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation and copy mode for reliable container builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1

# 1. Copy only lockfiles first to cache the dependency layer
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# 2. Copy the rest of the application and install the project
COPY . .
RUN uv sync --frozen

# Place the virtual environment on the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Run your application (adjust to your entrypoint, e.g., uvicorn or python -m)
CMD ["uvicorn", "pasly_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

