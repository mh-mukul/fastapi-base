FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (optional if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy all app source code
COPY . .

# Run entrypoint
ENTRYPOINT ["bash", "docker-entrypoint.sh"]
