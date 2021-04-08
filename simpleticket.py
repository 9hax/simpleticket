# SimpleTicket main app file


# Handle Imports
from flask import *
from flask_migrate import Migrate
import config, json, user, git

#from models import db

# prepare language files

with open("lang/"+config.LANGUAGE+".json",'r',encoding="utf-8") as langfile:
    lang = json.load(langfile)

# get current git commit shortname to display in the about page

version = git.Repo(search_parent_directories=True).head.object.hexsha[0:7]

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simpleticket.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.init_app(app)
#Migrate(app, db)

# make some variables available to the templating engine
@app.context_processor
def global_template_vars():
    return {
        "sitename": config.SITE_NAME,
        "lang": lang,
        "stversion": version
    }

# set a custom 404 error page to make the web app pretty
@app.errorhandler(404)
def pnf(e):
    return render_template('404error.html')

# the index and landing page. this displays all the active and closed tickets.
@app.route('/')
def home():
    return render_template('index.html')

# the about page. this shows the current software version and some general information about SimpleTicket.
@app.route('/about')
def about():
    return render_template('about.html')

# the login page. this allows a user to authenticate to enable them to create and edit tickets.
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        if request.form["login"] == 'test-user':
            return redirect(url_for('home'))
        else: 
            message = lang["login-error"]
    return render_template('login.html', message = message)

# provide a logout url. we dont want users to get stuck logged in :)
@app.route('/logout')
def logout():
    return 'notimplemented'

# the password reset page to enable the users to reset their own password, provided they know their own email address.
@app.route('/pwreset', methods=['GET', 'POST'])
def resetPW():
    message = None
    if request.method == 'POST':
        message = lang['password-reset-form-message']
        user.resetpw(request.form["email"])
    return render_template('pwreset.html', message = message)
