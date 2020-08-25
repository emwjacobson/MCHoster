FROM openjdk:11.0-jre-buster

ENV MC_VERSION 1.16.1
ENV PAPER_BUILD "latest"
ENV RAM 1G

WORKDIR /server

EXPOSE 25565/tcp
EXPOSE 25565/udp

RUN apt-get update && \
    apt install -y --no-install-recommends wget && \
    rm -rf /var/lib/apt/lists/*

COPY setup.sh .
COPY data .

CMD ["sh", "./setup.sh"]
