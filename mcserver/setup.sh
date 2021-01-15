# Download and accept EULA
if [ ! -f server.jar ]; then
    wget ${PAPER_DOWNLOAD_URL} -O server.jar
    echo "eula=true" > eula.txt
fi

# Run server
echo "op ${OP_USERNAME}" | java -Xms${RAM} -Xmx${RAM} -jar server.jar nogui