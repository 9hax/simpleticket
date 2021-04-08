# main file for a simple open source ticketing system
# written from scratch by 9hax
# this uses the flask framework

from flask import *
from flask_migrate import Migrate
import config, json, user, git

from models import db

# prepare language files

with open("lang/"+config.LANGUAGE+".json",'r',encoding="utf-8") as langfile:
    lang = json.load(langfile)

# get current git commit version

version = git.Repo(search_parent_directories=True).head.object.hexsha[0:7]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simpleticket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Migrate(app, db)

@app.context_processor
def global_template_vars():
    return {
        "sitename": config.SITE_NAME,
        "lang": lang,
        "stversion": version
    }

@app.errorhandler(404)
def pnf(e):
    return render_template('404error.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        if request.form["login"] == 'test-user':
            return redirect(url_for('home'))
        else: 
            message = lang["login-error"]
    return render_template('login.html', message = message)

@app.route('/logout')
def logout():
    return 'notimplemented'

@app.route('/pwreset', methods=['GET', 'POST'])
def resetPW():
    message = None
    if request.method == 'POST':
        message = lang['password-reset-form-message']
        user.resetpw(request.form["email"])
    return render_template('pwreset.html', message = message)