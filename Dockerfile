FROM python:3.11-slim

WORKDIR /app

COPY optimus_portal_cloud/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY optimus_portal_cloud/main.py .

ENV PORT=8080
CMD ["python", "main.py"]
