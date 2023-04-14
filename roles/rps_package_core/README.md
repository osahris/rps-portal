# RPS Core Package

This role installs every service to get a minimal functional installation of the RPS up and running.

It includes the following roles and installs the following services:

- Docker
    - Installs docker and docker-compose
    - See the documentation of the docker role.
- Gitlab credentials
    - Provides gitlab credentials for access to protected docker images
    - See the documentation of the gitlab_credentials role.
- Traefik
    - Installs a traefik reverse-proxy that is used to route traffic to the other services
    - Provides a docker network called proxy that is used by the other services to communicate with traefik
    - Provides a dashboard that can be accessed at the subdomain traefik.
    - See the documentation of the traefik role.
- Keycloak
    - Installs a Keycloak service at the subdomain accounts.
    - See the documentation of the keycloak role.
- Keycloak Realms
    - Configures a keycloak realm
    - See the documentation of the keycloak_realms role.
- oauth2-proxy
    - Installs an oauth2-proxy service at the subdomain oauth2.
    - See the documentation of the oauth2-proxy role.
- redirects
    - Allows to configure redirects from one url to another
    - See the documentation of the redirects role.
