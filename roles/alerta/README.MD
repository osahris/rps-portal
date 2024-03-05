# Ansible role for the Alerta monitoring tool 
Implementeed as a Docker container under the reverse proxy by Traefik service.


# How to use

The following credentials should be defined in the Ansible secrets, e.g., in './inventory/group_vars/monitoring_servers/secrets.yaml':
1. alerta_admin_api_key - creates an additional custom admin-scope API key(s). By default one key is generated randomly.
2. alerta_admin_password - sets a defined password for an initial admin acount. If not set, a default 'alerta' password is initially used for all admins
3. alerta_admin_api_key_cli - an initial key to perform actions via terminal. By default a random value is used which can be found in the 'alerta.conf' file after deployment
4. alerta_secret_key - an initial key to encode tokens and API keys. By default a random value is used which can be found in the 'alertad.conf' file after deployment

Note that the 'alerta.conf.j2' and 'alertad.conf.j2' should not be templated by Ansible because it will be done by Alerta itself at the deployment stage.

To add a new admin user from a Terminal, use the following command:

*alertad key --username <name> --key <alerta_API_KEY> --duration 315360000 --text 'Monitoring services' --scope 'read' --scope 'write:alerts' --scope 'read:alerts'*

Duration is set in seconds, 10 years = 315360000 seconds. A comment section like 'Monitoring services' is optional. Each scope is defined separately.


# How to add plugins

1. Put the files with a plugin to './files/plugins/<plugin_name>/'.
2. Configure requiered parameters in the plugin folder.
3. In the './templates/docker-compose.yaml.j2' modify the 'PLUGINS' environment variable and maybe make other plugin-related changes.
4. Modify the './files/Dockerfile' adding a layer 'RUN pip install /app/plugins/<plugin_name>/'.
5. Add the plugin settings to the './files/alertad.conf.j2' template file.

# Matrix plugin

A custom implementation of the plugin for creating automatic messages to a Matrix Element chat is included.

The following credentials should be defined in the Ansible secrets, e.g., in './inventory/group_vars/monitoring_servers/secrets.yaml':

1. alerta_matrix_homeserver - a server hosting the user who sends messages about alerts. Can be found in Matrix in 'User Settings - Help & About - Advanced - Homeserver'
2. alerta_matrix_access_token - a token for a user that sends the messages about alerts. Can be found in Matrix in 'User Settings - Help & About - Advanced - Access Token'.
3. alerta_matrix_room_ID - a chat room where the messages about alerts should be sent. Can be found in Matrix in 'Room Settings - Advanced - Room information - Internal room ID'.


In './files/plugins/matrix', each change from original is labeled as 'custom block'. In particular, a custom feature is that alerts with severities listed in the variable 'MATRIX_IGNORE_SEVERITY' will not be reported.