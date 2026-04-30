FROM python:3.11.3-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENV FLASK_APP=api/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH=/app

ENTRYPOINT ["./entrypoint.sh"]