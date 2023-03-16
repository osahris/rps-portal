####################
# Tulsky V.A. 2023 #
####################
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

@app.route('/')
def home():
    servicename = request.args.get('app')
    domain = os.environ.get("HOST_DOMAIN")
    services = [{'name': 'Budibase',                'subdomain': 'budibase'},
                {'name': 'Header',                  'subdomain': 'header'},
                {'name': 'Header (static)',         'subdomain': 'static-header-test'},
                {'name': 'IDIA',                    'subdomain': 'idia'}, 
                {'name': 'Keycloak',                'subdomain': 'keycloak'},
                {'name': 'Matchmaking',             'subdomain': 'matchmaking'},
                {'name': 'MVP',                     'subdomain': 'mvp'},
                {'name': 'Nextcloud',               'subdomain': 'nextcloud'},
                {'name': 'OpenProject',             'subdomain': 'openproject'},
                {'name': 'RocketChat',              'subdomain': 'rocketchat'},
                {'name': 'rps_admin_interface',     'subdomain': 'admin'},
                {'name': 'rps_groups_interface',    'subdomain': 'groups',       'path': 'realms/rps'},
                {'name': 'Traefik',                 'subdomain': 'traefik'},
                {'name': 'Wiki Bookstack',          'subdomain': 'wiki-bookstack'},
                {'name': 'Wiki.js',                 'subdomain': 'wiki-js'},
                {'name': 'Wordpress (Dev)',         'subdomain': 'www-staging'},
                {'name': 'Wordpress (Prod)',        'subdomain': 'www'},
                ]
    success = False
    for element in services:
        if servicename == element['subdomain']:
            success = True
            service = element
            title = "{} | NUM Hub".format(service['name'])
            return render_template('index.html',title = title,
                                    domain = domain,
                                    service=service)
    if success == False:
        return render_template('errors/service_not_found.html')

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

def service_not_found(e):
    title = "Service Not Found"
    return render_template('errors/service_not_found.html', 
                            title = title)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port)