####################
# Tulsky V.A. 2023 #
####################
from flask import Flask, render_template, request, redirect
import requests
import os

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():
    title = "RPS Services Navigator"
    domain = os.environ.get("HOST_DOMAIN")
    # upperdomain = '.'.join(domain.split('.')[1:])
    services = [{'name': 'Budibase',                'subdomain': 'base'},
                {'name': 'Gitea',                   'subdomain': 'code'},
                {'name': 'Header',                  'subdomain': 'header'},
                {'name': 'Header (static)',         'subdomain': 'static-header-test'},
                {'name': 'Keycloak',                'subdomain': 'accounts'},
                {'name': 'MatrixChat',              'subdomain': 'element.chat'},
                {'name': 'MVP',                     'subdomain': 'mvp'},
                {'name': 'Nextcloud',               'subdomain': 'cloud'},
                {'name': 'OpenProject',             'subdomain': 'openproject'},
                {'name': 'RocketChat',              'subdomain': 'rocketchat'},
                {'name': 'rps_admin_interface',     'subdomain': 'admin'},
                # {'name': 'rps_navigator',           'subdomain': 'navigator'}, 
                {'name': 'rps_people',              'subdomain': 'people'},
                {'name': 'rps_groups_interface',    'subdomain': 'groups',       'path': 'realms/rps'},
                {'name': 'Traefik',                 'subdomain': 'traefik'},
                {'name': 'Wiki Bookstack',          'subdomain': 'wiki'},
                {'name': 'Wiki.js',                 'subdomain': 'wiki-js'},
                {'name': 'Wordpress (Draft)',       'subdomain': 'www-draft'},
                {'name': 'Wordpress (Live)',        'subdomain': 'www'},
                ]
    for service in services:
        url_protocol = 'https'
        url =  url_protocol + "://"
        if 'subdomain' in service:
            url += service['subdomain'] + '.'
        url += domain 
        if 'path' in service:
            url += '/' + service['path']
        try:
            status_code = requests.head(url,timeout=1).status_code
        except:
            status_code = '404'
        service['received_code'] = status_code
    return  render_template('index.html', 
                            title = title,
                            domain = domain,
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
