# Things I should do eventually

## General
- Readme instructions
- Per-component Readmes

## Manager
- Remove /stop/all endpoint
- Volumes - limit size?
- If another container was started too recently, dont start a new one - prevents from overlapping CPU heavy tasks
- Use `username` as the OP on the server
- If a volume hasent been used in >= 5 days(?) delete the volume to conserve space

## MCServer
- Apply optimizations: https://www.spigotmc.org/threads/guide-server-optimization%E2%9A%A1.283181/

## Web
- Use Docker secrets for the db password
- Add ability to start server with a username

## Database
- Use Docker secrets for the password
