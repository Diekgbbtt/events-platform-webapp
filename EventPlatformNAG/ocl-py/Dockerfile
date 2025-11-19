# Alpine-based multi-stage build for minimum size
FROM python:3.11-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    make \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    openssl-dev \
    openjdk11-jdk

# Copy build files
COPY requirements.txt Makefile OclExpression.g4 setup.py ./
COPY ocl/ ./ocl/
COPY tests/ ./tests/

# Build everything
RUN python3 -m venv .venv \
    && . .venv/bin/activate \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && make \
    && pip install --no-cache-dir . \
    && pip cache purge \
    && find /app/.venv -name "*.pyc" -delete \
    && find /app/.venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Runtime stage
FROM python:3.11-alpine AS runtime

WORKDIR /app

# Install only runtime dependencies
RUN apk add --no-cache openjdk11-jre-headless bash

# Copy only the virtual environment
COPY --from=builder /app/.venv /app/.venv

# Create non-root user
RUN addgroup -g 1001 ocluser && adduser -D -u 1001 -G ocluser ocluser \
    && chown -R ocluser:ocluser /app
USER ocluser

CMD ["/bin/bash", "-c", ". .venv/bin/activate && exec bash"]
