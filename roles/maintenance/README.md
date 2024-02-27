# Ansible role for a Maintenance webpage

This is a Maintenance page webserver running in a docker container. Based on Flask.
Runs under the reverse proxy from a Traefik container.
Deployable as an Ansible role.

# What does it do?

The webserver in this role displays the content of the `/files/templates/maintenance.html` file for all requests that come to domains listed in `/vars/main.yaml`.

# How to turn the maintenance on and off?

Switch the variable `activate_maintenance` in `/vars/main.yaml` between `True` and `False` and launch this Ansible role.
