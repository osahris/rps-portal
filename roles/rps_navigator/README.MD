# What is this Ansible Role:

The service provides a navigation webpage for easy access to other services in the RPS stack.
The service is running in a docker container under the reverse proxy from a Traefik container.

## How to use:

1. Set the SSL certificate provider by editing **traefik_certresolver** in **./vars/main.yaml**. E.g., **letsencrypt-staging** for development, **letsencrypt** for production.

2. Use the docker network **proxy** to connect with Traefik, use the network **{{project_name}}** for internal communications of docker containers out of scope of Traefik.

3. By default, the service will run under the domain **https://{{rps_navigator_service_name}}** as defined in **./vars/main.yaml** by the following code:
   ```yaml
   # ./vars/main.yaml
   traefik_dynamic_config:
     http:
       routers:
         rps_navigator:
           rule: "Host(`{{rps_navigator_service_name}}`)"
   ```
