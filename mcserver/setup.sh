#!/bin/bash

MAJOR_VERSION=${MC_MAJOR_VERSION}
DATA=$(curl -s -X GET "https://papermc.io/api/v2/projects/paper/version_group/1.16/builds" -H  "accept: application/json")
VERSION=$(echo ${DATA} | jq -r '.builds[-1].version')
BUILD=$(echo ${DATA} | jq -r '.builds[-1].build')

DOWNLOAD_URL="https://papermc.io/api/v2/projects/paper/versions/${VERSION}/builds/${BUILD}/downloads/paper-${VERSION}-${BUILD}.jar"

# Download and accept EULA
if [ ! -f server.jar ]; then
    wget ${DOWNLOAD_URL} -O server.jar
    echo "eula=true" > eula.txt
fi

# Run server
cat commands.txt | java -Xms${RAM} -Xmx${RAM} -jar server.jar nogui