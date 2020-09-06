FROM python:3.6

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    wget && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /bin && \
    chmod 755 /bin/wait-for-it.sh

COPY requirements.txt .
COPY mcweb mcweb
COPY web web
COPY manage.py .

RUN python3 -m pip install -r requirements.txt

RUN python3 manage.py collectstatic

RUN useradd user
RUN chown -R user:user /app
USER user

CMD wait-for-it.sh db:3306 -- gunicorn -w 4 -b 0.0.0.0:8000 mcweb.wsgi
