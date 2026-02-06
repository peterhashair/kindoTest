# Backend Dockerfile for FastAPI
FROM python:3.11-slim


# Set work directory
WORKDIR /app

# Install PostgreSQL client for wait-for-postgres.sh
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Make wait script executable
RUN chmod +x /app/wait-for-postgres.sh

# Start FastAPI app after waiting for db
ENTRYPOINT ["/app/wait-for-postgres.sh", "db"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
