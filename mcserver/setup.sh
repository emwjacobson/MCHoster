# Download and accept EULA
wget https://papermc.io/api/v1/paper/${MC_VERSION}/${PAPER_BUILD}/download -O server.jar
java -jar server.jar
sed -i 's/false/true/g' eula.txt

# Run server
java -Xms${RAM} -Xmx${RAM} -jar server.jar nogui