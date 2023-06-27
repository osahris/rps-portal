# Keycloak Registration Mail Password
After every run of keycloak role, the following steps are performed:
```bash	
nano /etc/ansible/facts.d/accounts.dev.numhub.de.fact
```
Set to the following value:
```json
{
  "keycloak_registration_mail_server_config_password": "password"
}
```