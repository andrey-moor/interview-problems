# Dockerfile for Merkle Tree Sync Server
#
# Build from starter/ directory:
#   docker build -t merkle-sync-server -f server/Dockerfile .
#
# Run:
#   docker run -p 8000:8000 merkle-sync-server

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY common ./common
COPY server/main.py .

# Run the server
EXPOSE 8000
CMD ["python", "main.py"]
