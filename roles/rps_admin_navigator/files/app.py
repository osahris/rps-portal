####################
# Tulsky V.A. 2023 #
####################
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():
    title = "RPS Services Navigator"
    domain = os.environ.get("HOST_DOMAIN")
    upperdomain = '.'.join(domain.split('.')[1:])
    services = [{'name': 'Budibase',                'subdomain': 'budibase'},
                {'name': 'Header',                  'subdomain': 'header'},
                {'name': 'Header (static)',         'subdomain': 'static-header-test'},
                {'name': 'Keycloak',                'subdomain': 'keycloak'},
                {'name': 'rps_people',              'subdomain': 'people'},
                {'name': 'MVP',                     'subdomain': 'mvp'},
                {'name': 'Nextcloud',               'subdomain': 'nextcloud'},
                {'name': 'OpenProject',             'subdomain': 'openproject'},
                {'name': 'RocketChat',              'subdomain': 'rocketchat'},
                {'name': 'rps_admin_interface',     'subdomain': 'admin'},
                {'name': 'rps_admin_navigator',     'subdomain': 'navigator'}, 
                {'name': 'rps_groups_interface',    'subdomain': 'groups',       'path': 'realms/rps'},
                {'name': 'Traefik',                 'subdomain': 'traefik'},
                {'name': 'Wiki Bookstack',          'subdomain': 'wiki-bookstack'},
                {'name': 'Wiki.js',                 'subdomain': 'wiki-js'},
                {'name': 'Wordpress (Draft)',       'subdomain': 'www-draft'},
                {'name': 'Wordpress (Live)',        'subdomain': 'www'},
                ]
    return  render_template('index.html', 
                            title = title,
                            domain = upperdomain,
                            services = services)

@app.errorhandler(404)
def page_not_found(e):
    title = "Page Not Found"
    return render_template('errors/404.html', 
                            title = title), 404

@app.errorhandler(500)
def internal_server_error(e):
    title = "Internal Server Error"
    return render_template('errors/500.html', 
                            title = title), 500



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)
