# Research Project Suite

TBD Description

## Deploy!

```
ansible-playbook -i inventory/common/ -i inventory/environments/dev/ deploy-all-services.yaml
```

# Services

The [x]-marked roles are ready to be deployed within one button click, without further pre-adjustments:

- [ ] budibase
- [x] collabora
- [ ] discourse
- [x] keycloak_themes
- [x] docker
- [x] keycloak
- [x] keycloak_realms
- [ ] rps_people
- [x] matrix
- [x] minimum_viable_product
- [x] nextcloud
- [x] oauth2_proxy
- [ ] openproject
- [ ] proskive
- [ ] rocketchat
- [x] rps_admin_interface
- [x] rps_admin_navigator
- [ ] rps_cohort_explorer
- [x] rps_groups_interface
- [x] rps_header
- [x] rps_style_server
- [ ] rps_sync_services
- [ ] socat_https_proxy
- [x] traefik
- [ ] typesense
- [x] wiki_bookstack
- [x] wiki_js
- [ ] wordpress

## Add a new service

The quick way to add a new service is to copy the `minimum_viable_product` folder and follow the instructions in the `README.md` inside. Do not forget to include it in the services list above and mark with [ ] when in progress or with [x] when fully ready to be deployed.

## Secrets management

Secrets are stored on the remote machine in `/etc/ansible/facts.d/secrets.fact`. Most things like database passwords etc. just need to be generated once per machine but we don't really care about the exact password.

However for some externally defined secrets like the shared gitlab deploy token password the user will be asked to provide it via an interactive prompt. Should you make a typo or has it been changed externally it is possible to specify the new password via ansible extra vars:

```
ansible-playbook -i inventory-dev deploy-all-services.yaml  --tags=gitlab_credentials --extra-vars "gitlab_deploy_token_password=hurz"
```

## docker-compose deployments

Whenever possible try to deploy applications using `docker-compose`.

All application configs should reside below `/srv/`.

By convention please create a variable `($project_name)_service_name` (using `defaults`) and a variable `remote_path: "/srv/{{($project_name)_service_name}}"` (using `vars`) for the server name the application is reachable under.

Then in the tasks of your role ensure that the directory is being created and deploy all application configs including the `docker-compose.yaml` file in there.
Make sure that the application uses the well-known `proxy` network. This is the network that Traefik expects services to reside in.

Example config excerpt:

```yaml
    [...]
networks:
  proxy:
    external: true

services:
    myapp:
        image: ...
        networks:
            - proxy

```

Then in your tasks when deploying the docker-compose stack make sure to set `remove_orphans` and `pull` to true and make sure that you eventually restart the docker-compose stack if you deployed config files that are being mounted into the container that are not automatically picked up by the application.

Example:

```yaml
- name: deploy docker-compose stack
  docker_compose:
    project_src: "{{remote_path}}"
    remove_orphans: true
    restarted: "{{ myapp_copy_static_config_task.changed }}"
    pull: true
```

Changes in the docker-compose file will automatically trigger a restart (please do not change the default ansible `recreate` setting).

To make your application known to Traefik create a traefik configuration in `/srv/traefik/conf.d/$project_name.yaml` using a variable defined in `$role/vars/main.yaml`.

Example config:

```yaml
myapp_traefik_dynamic_config:
  http:
    routers:
      myapp:
        rule: "Host(`{{myapp_service_name}}`)"
        entrypoints: websecure
        tls:
          certresolver: letsencrypt
        service: myapp

    services:
      myapp:
        loadBalancer:
          servers:
            - url: "http://{{myapp_service_name|replace('.','')}}_myapp_1"
```

## Undeploy!

Clean VM from all RPS related for a brand new setup:

```sh
docker ps -a --format "{{.Names}}" | grep -v '^traefik$' | xargs docker stop | xargs docker rm
docker volume prune
docker system prune
docker stop traefik
docker rm traefik
rm -r /srv
rm /etc/ansible/facts.d/ -R
```
