FROM python:3.11-slim

WORKDIR /app
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev

# Flask-app requirements
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r ./requirements.txt
