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
keycloak_realms:
  - name: users
    # groups that should be created in our realm
    groups:
      - test
      - test2
    # roles that should be created in our realm
    roles:
      - testrole
    external_idps:
      - alias: "external-identity-provider"
        display_name: "External"
        client_id: "external"
        client_secret: "ClientSecretFromIdP"
        authorization_url: "https://example.com/realms/users/protocol/openid-connect/auth"
        token_url: "https://example.com/realms/users/protocol/openid-connect/token"
        userinfo_url: "https://example.com/realms/users/protocol/openid-connect/userinfo"
        issuer: "https://example.com/realms/users"
        sync_mode: force
        import:
          # when the user is in "remote_group" they should be assigned role "testrole" in our realm
          # note that this requires a "groups" claim containing a list of groups (i.e. create a a client mapper with "Group Membership" on the remote keycloak)
          - name: "testrole"
            type: "role_from_group"
            from_group: "remote_group"
          # group "test" should be assigned when user is in "test" group on the remote side
          - name: "test"
            type: "group"
          # group "test2" should be assigned when user is in "test" group on the remote side. from defaults to name of group
          - name: "test2"
            type: "group"
            from: "test"
  - name: subrealm
    # subrealm is a subrealm. so it doesn't have its own login form but redirects to the parent_realm and imports users from there
    parent_realm:
      # name of parent_realm (on the same keycloak server)
      name: users
      # whatever secret you want. use ansible_vault or something else
      client_secret: "clientsecret"
      import:
        # import user attribute "title" from parent_realm
        - name: "title"
          type: "attribute"
        # import test group from parent_realm
        - name: "test"
          type: "group"
        # import test2 group from group test in parent_realm
        - name: "test2"
          type: "group"
          from: "test"
        # assign "test" role when user is in "test2" group in parent_realm
        - name: "test"
          type: "role_from_group"
          from_group: "test2"
      # user must be in group "test" or "test2" (you probably need to somehow import it - see above - or set it manually after initial import)
      required_groups:
        - "test"
        - "test2"
      # same just for roles
      required_roles:
        - "test"
    groups:
      - "test"
    roles:
      - "test"
```

### Possible import types

Imports can be used in external_idps or when a realm has a parent_realm

```yml
# import user attribute "title" from parent_realm
- name: "title"
  type: "attribute"
```

```yml
# group "test" should be assigned when user is in "test" group on the remote side
# from is optional and defaults to "name"
- name: "test"
  type: "group"
  from: "test"
```

```yml
# when the user is in "remote_group" they should be assigned role "testrole" in our realm
- name: "testrole"
  type: "role_from_group"
  from_group: "remote_group"
```

## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
