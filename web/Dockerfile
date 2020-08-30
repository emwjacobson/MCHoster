FROM python:3.6

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY mcweb mcweb
COPY web web
COPY manage.py .

RUN python3 -m pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:80 mcweb.wsgi
