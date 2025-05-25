# Build stage
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy just requirements first to leverage caching
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-slim

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

WORKDIR /src

# Copy application code
COPY /src .

# Make sure to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 3775

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3775"]