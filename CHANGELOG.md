# Changelog of RPS Portal

## Unreleased

- Added onlyoffice role

## Release v2.0.0

Complete rewrite of the Research Project Suite (RPS) project.

- We now use Docker and docker-compose for all application deployments with a unified directory structure on the target machine.
- We now use Traefik as the reverse proxy.
- We added oauth2-proxy as an authentication proxy so 
- Adds the ability to deploy all RPS apps in a single command on a single machine.
- Faster deployments then before.
- Now we have standard packages with defaults for most of the configuration so you don't need to configure a lot for the projects individually.
