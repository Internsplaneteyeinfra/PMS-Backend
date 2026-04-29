FROM python:3.11-slim

# Env vars
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings_prod

WORKDIR /app

# Only libpq-dev needed at runtime for psycopg2-binary
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Media dir + entrypoint
RUN mkdir -p /app/media \
    && chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
