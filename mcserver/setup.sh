# Download and accept EULA
if [ ! -f server.jar ]; then
    wget https://papermc.io/api/v1/paper/${MC_VERSION}/${PAPER_BUILD}/download -O server.jar
    echo "eula=true" > eula.txt
fi

# Run server
echo "op ${OP_USERNAME}" | java -Xms${RAM} -Xmx${RAM} -jar server.jar nogui