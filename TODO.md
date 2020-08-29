# Things I should do eventually

## General
- Readme instructions
- Per-component Readmes
- Look into running Django and Flask in Production

## Manager
- Remove /stop/all endpoint
- Volumes - limit size?
- If another container was started too recently, dont start a new one - prevents from overlapping CPU heavy tasks
- If a volume hasent been used in >= 5 days(?) delete the volume to conserve space

## MCServer

## Web
- Use Docker secrets for the db password
- Add ability to start server with a username

## Database
- Use Docker secrets for the password
