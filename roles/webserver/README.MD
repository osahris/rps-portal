# What is this Ansible role

This is a webserver application that provides the layout for the RPS website combining the RPS Header, Footer and the frame with content.
The service is running in a docker container under the reverse proxy from a Traefik container.


## How to use:

1. Set the SSL certificate provider by editing **traefik_certresolver** in **./vars/main.yaml**. E.g., **letsencrypt-staging** for development, **letsencrypt** for production.

2. Use the docker network **proxy** to connect with Traefik, use the network **{{project_name}}** for internal communications of docker containers out of scope of Traefik.

3. By default, the service will run under the domain **https://{{webserver_service_name}}** as defined in **./vars/main.yaml** by the following code:
    ```yaml
    # ./vars/main.yaml
    traefik_dynamic_config:
      http:
        routers:
          webserver:
            rule: "Host(`{{webserver_service_name}}`)"
    ```