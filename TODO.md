# Things I should do eventually

## General
- Readme instructions
- Per-component Readmes

## Manager
- Remove /stop/all endpoint
- Volumes - limit size?
- If another container was started too recently, dont start a new one - prevents from overlapping CPU heavy tasks
- Use `username` as the OP on the server
- Add ability to reset map of username
    - Stop containers
    - Delete `username` volume
    - Restart?

## MCServer

## Web
- Use Docker secrets for the db password
- Add ability to start server with a username

## Database
- Use Docker secrets for the password
