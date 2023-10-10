####################
# Tulsky V.A. 2023 #
####################
from flask import Flask, render_template, request, redirect
import requests
import os
import yaml

# Read YAML file
def read_yaml_file(filename):
    with open(filename, 'r') as file:
        data = yaml.safe_load(file) # returns a dictionary
    return data

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():
    title = "RPS Services Navigator"
    domain = os.environ.get("HOST_DOMAIN")
    # upperdomain = '.'.join(domain.split('.')[1:])

    script_dir = os.path.dirname(__file__) # Get the absolute path to the current script
    services_data = read_yaml_file(os.path.join(script_dir, "services.yaml"))
    services = []
    for service in services_data.get('services'):
        url_protocol = 'https'
        url =  url_protocol + "://"
        if 'subdomain' in service:
            url += service.get('subdomain') + '.'
        if 'domain' in service:
            url += service.get('domain')
        else:
            url += domain
        if 'path' in service:
            url += '/' + service.get('path')
        try:
            status_code = requests.head(url,timeout=1).status_code
        except:
            status_code = '404'
        service['received_code'] = status_code
        service['url'] = url
        services.append(service)
    return render_template('index.html', 
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
