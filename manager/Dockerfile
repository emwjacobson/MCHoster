FROM ubuntu:20.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common \
        cron && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /manager

COPY app.py .
COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY data/server-cleaner /etc/cron.d/server-cleaner
RUN chmod 0644 /etc/cron.d/server-cleaner
RUN crontab /etc/cron.d/server-cleaner
# RUN service cron start

# RUN useradd user
# RUN usermod -aG docker user

# USER user

CMD cron && gunicorn -w 4 -b 0.0.0.0:8000 app:app
