
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip --default-timeout=300 --retries=10 install --no-cache-dir -r requirements.txt

COPY main.py .
COPY student_performance_model.joblib .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
