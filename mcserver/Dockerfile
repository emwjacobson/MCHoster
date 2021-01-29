FROM openjdk:11.0-jre-buster
STOPSIGNAL SIGTERM

ENV MC_MAJOR_VERSION 1.16
ENV RAM 1G

WORKDIR /server

RUN apt-get update && \
    apt install -y --no-install-recommends wget jq && \
    rm -rf /var/lib/apt/lists/*

COPY setup.sh .
COPY data .
COPY commands.sh .

RUN chmod +x setup.sh
RUN chmod +x commands.sh
RUN useradd user
RUN chown -R user:user /server

USER user

CMD [ "/server/setup.sh" ]
