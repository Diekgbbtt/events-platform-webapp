FROM python:3.11-slim

WORKDIR /project
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    sqlite3

# Flask-app requirements
COPY . .
RUN pip3 install -e .
