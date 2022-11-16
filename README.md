# Role Name

Configures subrealms in keycloak that are autoconfigured to use a mainrealm as an idp and sync some attributes from it

## Requirements

A working keycloak with a mainrealm

## Role Variables

- keycloak_admin_username

  username to use for authenticating against keycloak. defaults to admin

- keycloak_admin_password

  password to use for authenticating against keycloak.

- keycloak_auth_realm

  realm to use for authenticating as `keycloak_admin_username`. defaults to `master`

- keycloak_main_realm_name

  realm name used as root realm for all subrealms. defaults to `users`

- keycloak_validate_certs

  if certs should be validated. useful for self signed certs. should always be true on prod systems. defaults to `true`

- keycloak_frontend_url

  keycloak url to use. http://localhost:8080

- keycloak_subrealms

  list that contains all subrealms and their config. see "Example playbook"

- keycloak_subrealm_client_secrets

  dict&lt;SubRealmName, ClientPassword&gt;

## Dependencies

## Example Playbook

```yml
---
# we are executing against keycloak_frontend_url. no need to do ssh
- hosts: localhost
  roles:
    - role: keycloak-subrealms
      # should be placed in a vault file
      keycloak_admin_password: admin
      keycloak_subrealm_client_secrets:
        peng: oa3hai9eiJ9ooxeiR8phaem0jieroh2g
        puff: aip9pau1leiW7aighieth9aisho4push

      keycloak_frontend_url: http://localhost:8080
      keycloak_subrealms:
        - name: peng
          client_secret: "{{ keycloak_subrealm_client_secrets['peng'] }}"
          required_group: perdauz
          # list of all attributes you want to import. standard attributes like email, firstname etc are automatically imported
          import:
            - name: title
              type: "attribute"
        - name: puff
          client_secret: "{{ keycloak_subrealm_client_secrets['puff'] }}"
```

## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
