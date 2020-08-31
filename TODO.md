# Things I should do eventually

## General
- Readme instructions
- Per-component Readmes
- Look into running Django and Flask in Production
- Docker-compose
- Implement some kinda CI?

## Manager
- Remove /stop/all endpoint
- Volumes - limit size?
- If another container was started too recently, dont start a new one - prevents from overlapping CPU heavy tasks
- If a volume hasent been used in >= 5 days(?) delete the volume to conserve space
- When resetting, check if container too new

## MCServer
- When new version of MC is available, but existing volume exists (with old MC version), download new jar

## Web
- Use Docker secrets for the db password
- Add pages
    - Stop server
    - Reset server
- SSL
- Set Django SECRET_KEY to environment variable

## Database
- Use Docker secrets for the password
