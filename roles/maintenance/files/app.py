#########################
# Tulsky V.A. 2024 #
#########################
from flask import Flask, render_template, abort, redirect
import os

app = Flask(__name__)

@app.route('/')
def home():
    abort(503)

@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

@app.errorhandler(500)
def internal_server_error(e):
    return redirect("/")

@app.errorhandler(503)
def maintenance(e):
    return render_template('maintenance.html'), 503

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(debug=False, host='0.0.0.0', port=port)
