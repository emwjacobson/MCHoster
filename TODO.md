# Things I should do eventually

## General
- Per-component Readmes
- Implement some kinda CI?
- Have Dockerfiles run as normal user

## Manager
- Add settings to be environmental variables
- Volumes - limit size?
- If a volume hasent been used in >= 5 days(?) delete the volume to conserve space
- When resetting, check if container too new?
    - Check is normally to prevent world corruption, but if its being deleted, does it matter?

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
