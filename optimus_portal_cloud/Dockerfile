FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y chromium-browser chromium-browser-sandbox && rm -rf /var/lib/apt/lists/*
COPY optimus_portal_cloud/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY optimus_portal_cloud/main.py main.py
COPY fiber_hunter.py .
COPY THEMAPMAN.py .
COPY hunter_dot_extractor.py .
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "main:app"]
