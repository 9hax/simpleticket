# main file for a simple open source ticketing system
# written from scratch by 9hax
# this uses the flask framework

from flask import *
import config 

app = Flask(__name__)

@app.context_processor
def global_template_vars():
    return {
        "sitename": config.SITE_NAME
    }

@app.route('/')
def printTickets():
    return render_template('index.html', username="Textuser")
