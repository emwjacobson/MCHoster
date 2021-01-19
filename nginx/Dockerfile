FROM nginx:1.19

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /bin && \
    chmod 755 /bin/wait-for-it.sh

COPY ./scripts/ /docker-entrypoint.d/
COPY ./data/default.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]