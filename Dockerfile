# Simple container for the Task Tracker CLI
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy source
COPY src/ ./src/

# No third-party deps required for runtime
# If you later add deps, copy requirements and install here.

CMD ["python", "src/main.py"]
