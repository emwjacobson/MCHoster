FROM openjdk:11.0-jre-buster

ENV MC_VERSION 1.16.2
ENV PAPER_BUILD "latest"
ENV RAM 1G

WORKDIR /server

RUN apt-get update && \
    apt install -y --no-install-recommends wget && \
    rm -rf /var/lib/apt/lists/*

COPY setup.sh .
COPY data .

RUN useradd user
RUN chown -R user:user /server

USER user

CMD ["sh", "./setup.sh"]
