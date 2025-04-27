FROM python:3.11-slim

# Install ghostscript
RUN apt-get update && \
    apt-get install -y ghostscript && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./
# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy the rest of the application code
COPY . .
# Expose the port the app runs on
EXPOSE 8000
# Start the FastAPI application
CMD ["fastapi", "run", "backend/main.py"]