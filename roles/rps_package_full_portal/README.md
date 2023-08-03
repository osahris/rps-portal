# RPS Core Package

This role installs every service to get a minimal functional installation of the RPS up and running.

It includes the following roles and installs the following services:

## General services
- Docker
    - Installs docker and docker-compose
    - See the documentation of the docker role.
- Traefik
    - Default adress: traefik.<domain_name>
    - Installs a traefik reverse-proxy that is used to route traffic to the other services
    - Provides a docker network called proxy that is used by the other services to communicate with traefik
    - Provides a dashboard that can be accessed at the subdomain traefik.
    - See the documentation of the traefik role.
- Keycloak
    - Default adress: accounts.<domain_name>
    - Installs a Keycloak service for single-sign-on (SSO)
    - See the documentation of the keycloak role.
- Keycloak Realms
    - Configures a keycloak realm used to provide single-sign-on 
    - See the documentation of the keycloak_realms role.
- oauth2-proxy
    - Default adress: oauth2.<domain_name>
    - Installs an oauth2-proxy service
    - See the documentation of the oauth2-proxy role.

## Optional general services

- Style server
    - Default adress: style.<domain_name>
    - Installs a web server that stores common CSS style files and degign elements for functional services and the header
- Header
    - Default adress: header.<domain_name>
    - Installs a web server with common header that can be integrated into functional services
- Keycloak Sync
    - Installs a service that syncronizes the roles and groups between Keucloak and functional services

## Functional services
- Matrix chat
    - Default adress: element.chat.<domain_name>
    - Installs a chat based on Matrix Synapse server and an Element Web client
    - See the documentation of the matrix role.
- Nextcloud
    - Default adress: cloud.<domain_name>
    - Installs a cloud providing data sharing, file editing with OpenOffice
    - See the documentation of the nextcloud role.
- Wiki Bookstack
    - Default adress: wiki.<domain_name>
    - Installs a wiki-like knowlenge base for shared use and editing
- Gitea
    - Default adress: code.<domain_name>
    - Installs a local git repository to store and share codes, texts, manuals and their development history
- Navigator
    - Default adress: <domain_name>
    - TBD