# Things I should do eventually

## General
- Per-component Readmes
- Implement some kinda CI?

## Manager
- Add settings to be environmental variables
- Volumes - limit size?
- If another container was started too recently, dont start a new one - prevents from overlapping CPU heavy tasks
- If a volume hasent been used in >= 5 days(?) delete the volume to conserve space
- When resetting, check if container too new

## MCServer
- When new version of MC is available, but volume exists (with old MC version), download new jar
- Ability to select plugins?

## Web
- Use Docker secrets for the db password?
    - Currently using docker-compose yaml to set
- Add pages
    - Reset server
- Favicon?

## Database
- Use Docker secrets for the password?
    - Currently using docker-compose yaml to set
