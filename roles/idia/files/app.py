####################
# Tulsky V.A. 2023 #
####################
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
db_path = '/app/idia/db/'+'dbname'+'.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init database
db = SQLAlchemy(app)
app.app_context().push()

#Create database model
class Users(db.Model):
    id           = db.Column(db.Integer,     primary_key=True)
    name         = db.Column(db.String(200), nullable=False)  # max length 200, no blank value allowed
    date_created = db.Column(db.DateTime,    default=datetime.utcnow)
    # Create a return-string function
    def __repr__(self):
        return '<Name %r>' % self.id

db.create_all()

subscribers = []

value1 = 0

@app.route('/', methods=["POST", "GET"])
def home():
    title = "IDIA main page"
    var1_dict = {'key1': value1}
    return redirect('/navigation')

@app.route('/new')
def new():
    title = "IDIA new page"
    var1_dict = {'key1': value1}
    return render_template('new.html', 
                            title = title,
                            var1_dict=var1_dict)

@app.route('/users', methods=["POST", "GET"])
def users():
    title = "IDIA users page"

    if request.method == "POST":
        user_name = request.form["name"]
        new_user = Users(name=user_name) # add a new entry to the Users database
        # push to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')
        except:
            return redirect('/errors/db_error')
    else:
        users = Users.query.order_by(Users.date_created)
        return render_template('users.html', 
                            title = title, users=users)

@app.route('/errors/db_error')
def db_error():
    title = "Database error"
    return render_template('errors/db_error.html', 
                            title = title)

@app.route('/navigation')
def navigation():
    title = "RPS Services Navigation"
    domain = os.environ.get("HOST_DOMAIN")
    services = [{'name': 'Header',                  'subdomain': 'header'},
                {'name': 'Header (static)',         'subdomain': 'static-header-test'},
                {'name': 'IDIA',                    'subdomain': 'idia'}, 
                {'name': 'Keycloak',                'subdomain': 'keycloak'},
                {'name': 'Matchmaking',             'subdomain': 'matchmaking'},
                {'name': 'Minimum viable product',  'subdomain': 'mvp'},
                {'name': 'Nextcloud',               'subdomain': 'nextcloud'},
                {'name': 'OpenProject',             'subdomain': 'openproject'},
                {'name': 'rps_admin_interface',     'subdomain': 'admin'},
                {'name': 'rps_groups_interface',    'subdomain': 'groups',       'path': 'realms/rps'},
                {'name': 'Traefik',                 'subdomain': 'traefik'},
                {'name': 'Wiki Bookstack',          'subdomain': 'wiki-bookstack'},
                {'name': 'Wiki.js',                 'subdomain': 'wiki-js'},
                {'name': 'Wordpress (Dev)',         'subdomain': 'www-staging'},
                {'name': 'Wordpress (Prod)',        'subdomain': 'www'},
                ]
    return  render_template('navigation.html', 
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