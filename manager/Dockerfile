FROM ubuntu:18.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        python3 \
        python3-dev \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /manager

COPY manager.py .
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

ENV FLASK_APP manager.py

CMD [ "flask", "run", "--host=0.0.0.0" ]