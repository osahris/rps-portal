# Ansible role for a Maintenance webpage

This is a Maintenance page webserver running in a docker container. Based on NginX.
Runs under the reverse proxy from a Traefik container.
Deployable as an Ansible role.

# What does it do?

The webserver in this role displays the content of the `/503.html` page for all requests that come to `https://maintenance.your_domain` (or whatever is the value of `maintenance_service_name` in `vars/main.yaml`).