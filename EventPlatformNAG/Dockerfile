FROM python:3.11-slim

WORKDIR /app
SHELL ["/bin/bash", "-c"]

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    default-jre-headless

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN echo "source /opt/venv/bin/activate" >> ~/.bashrc

COPY . .
RUN pip install -r requirements.txt
RUN make clean && make grammars
RUN pip install ./ocl-py

CMD ["sleep", "infinity"]