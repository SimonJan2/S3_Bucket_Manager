FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY s3_manager.py .
COPY templates/ ./templates/

EXPOSE 5000

CMD ["python", "s3_manager.py"]
