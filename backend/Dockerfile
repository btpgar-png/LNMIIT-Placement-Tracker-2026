FROM python:3.12-slim AS base

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
WORKDIR /app/backend

# Create persistent data directory for SQLite database
# On Render, this will be in /opt/render/project/src/data
# On Docker, this will be in /app/data
RUN mkdir -p /app/data

# Expose FastAPI port
EXPOSE 8000

# ENV ADMIN_TOKEN should be provided at runtime (do not bake secrets)
# Initialize database on startup
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

