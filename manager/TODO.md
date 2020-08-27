# Things I should do eventually

- Remove /stop/all endpoint
- Volumes - limit size?
- For /stop check to see if the container is "too new" to end, eg while its still running the startup script and pidof java does not exist
- If container with volume already running, don't allow another container to start with same volume
- If another container was started too recently, dont start a new one - prevents from overlapping CPU heavy tasks