FROM python:3.6

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential

RUN python3 -m pip install -r requirements.txt
