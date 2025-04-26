FROM python:3.11-slim

# Install poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Set the working directory
WORKDIR /app
# Copy the poetry files
COPY pyproject.toml poetry.lock ./
# Install the dependencies
RUN poetry install --no-root
# Copy the rest of the application code
COPY . .
# Expose the port the app runs on
EXPOSE 8080
# Run the application
CMD ["gunicorn", "frontend.app:app", "-b", "0.0.0.0:8080", "--timeout", "120", "--workers", "4"]