# Research Project Suite

TBD Description

# Services

The [x]-marked roles are ready to be deployed within one button click, without further pre-adjustments:

- [x] collabora
- [ ] discourse
- [x] docker
- [x] idia
- [x] keycloak
- [x] keycloak-realms
- [ ] nextcloud
- [x] oauth2-proxy
- [ ] openproject
- [ ] proskive
- [x] rps_admin_interface
- [ ] rps_cohort_explorer
- [x] rps_groups_interface
- [ ] rps_style_servers
- [ ] rps_sync_services
- [ ] socat_https_proxy
- [x] traefik
- [ ] typesense
- [ ] wiki-bookstack
- [ ] wiki-js


## Secrets management

Secrets are stored on the remote machine in `/etc/ansible/facts.d/secrets.fact`. Most things like database passwords etc. just need to be generated once per machine but we don't really care about the exact password.

However for some externally defined secrets like the shared gitlab deploy token password the user will be asked to provide it via an interactive prompt. Should you make a typo or has it been changed externally it is possible to specify the new password via ansible extra vars:

```
ansible-playbook -i inventory-dev deploy-all-services.yaml  --tags=gitlab_credentials --extra-vars "gitlab_deploy_token_password=hurz"
```

