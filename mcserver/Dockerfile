FROM openjdk:11.0-jre-buster

ENV PAPER_DOWNLOAD_URL https://papermc.io/api/v2/projects/paper/versions/1.16.4/builds/416/downloads/paper-1.16.4-416.jar
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
