# docker-pdf-convert

Uses Docker compose to manage a frontend container and a backend container for inverting the colors of a PDF file.

Local application can be run via,

```bash
docker-compose build
docker-compose up
```

The backend should run on port `8000` and the frontend on port `8080`.

## Frontend

Frontend is a simple static HTML page that allows the user to upload a PDF file and download the inverted version. The frontend is served by a simple `nginx` HTTP server.

## Backend

Backend is a simple Flask application that uses `subprocess` to call `gs` (Ghostscript) to invert the colors of the PDF file. The backend is served by a simple `gunicorn` HTTP server, and has a single endpoint that accepts a PDF file and returns the inverted version, implemented using `fastapi`.
