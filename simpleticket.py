# SimpleTicket main app file


# Handle Imports
from flask import Flask, session, render_template, redirect, url_for, request, abort, g
from flask_migrate import Migrate
import sqlalchemy
import models as m

import config, json, user, git, os, time, datetime

# prepare language files

with open("lang/"+config.LANGUAGE+".json",'r',encoding="utf-8") as langfile:
    lang = json.load(langfile)

# get current git commit shortname to display in the about page

version = git.Repo(search_parent_directories=True).head.object.hexsha[0:7]

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simpleticket.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
m.db.init_app(app)
Migrate(app, m.db)

# make some variables available to the main script
@app.before_request
def initializeRequest():
    g.current_user = None
    if "login" in session.keys() and session['login']:
        g.current_user = user.get_user(session['acc_id'])

# make some variables available to the templating engine
@app.context_processor
def global_template_vars():
    return {
        "sitename": config.SITE_NAME,
        "lang": lang,
        "stversion": version,
        "current_user": g.current_user,
        "ticket_list": m.Ticket.query.all(),
        "ticket_replies": m.TicketReply.query.all(),
        "ctime": time.ctime,
        "getTime": user.getTime
    }

# set a custom 404 error page to make the web app pretty
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404error.html')

# set a custom 403 error page to make the web app pretty
@app.errorhandler(403)
def accessDenied(e):
    return render_template('403error.html')

# set a custom 500 error page to make the web app pretty
@app.errorhandler(500)
def serverError(e):
    return render_template('500error.html')

# the index and home landing page. this displays all the active and closed tickets.
@app.route('/')
def home():
    if config.REQUIRE_LOGIN:
        if "login" in session.keys() and session['login']:
            return render_template('index.html')
        else:
            return redirect(url_for("login"))
    else: 
        return render_template("index.html")

# the page to create a new ticket on.
@app.route('/create', methods=['GET', 'POST'])
def createTicket():
    if "login" in session.keys() and session['login']:
        if request.method == 'POST':
            user.create_ticket(request.form["ticket-title"], request.form["ticket-text"], None, g.current_user, None)
            return redirect(url_for('home'))
        return render_template('ticket-create.html')
    else:
        abort(403)

# the page to view and edit tickets.
@app.route('/view/<ticketid>', methods=['GET', 'POST'])
def viewTicket(ticketid):
    ticket = m.Ticket.query.filter_by(id = ticketid).first()
    if ticket == None:
        abort(404)
    if "login" in session.keys() and session['login']:
        if request.method == 'POST':
            ticket.assigned_to_id = request.form["new-assignee-id"]
            m.db.session.commit()
        ticket_replies = m.TicketReply.query.filter_by(main_ticket = ticket)
        return render_template('ticket-view.html', ticket = ticket, replies = ticket_replies)
    else:
        abort(403)

@app.route('/view/<ticketid>/close')
def closeTicket(ticketid):
    ticket = m.Ticket.query.filter_by(id = ticketid).first()
    if ticket == None:
        abort(404)
    if "login" in session.keys() and session['login']:
        if g.current_user.id == ticket.created_by_id or g.current_user.highPermissionLevel:
            ticket.is_open = False
            m.db.session.commit()
            return redirect(url_for('viewTicket', ticketid = ticketid))
        else:
            abort(403)
    else:
        abort(403)

@app.route('/view/<ticketid>/reopen')
def reopenTicket(ticketid):
    ticket = m.Ticket.query.filter_by(id = ticketid).first()
    if ticket == None:
        abort(404)
    if "login" in session.keys() and session['login']:
        if g.current_user.id == ticket.created_by_id or g.current_user.highPermissionLevel:
            ticket.is_open = True
            m.db.session.commit()
            return redirect(url_for('viewTicket', ticketid = ticketid))
        else:
            abort(403)
    else:
        abort(403)

@app.route('/view/<ticketid>/reply', methods=['POST'])
def createTicketReply(ticketid):
    if "login" in session.keys() and session['login']:
        if request.method == 'POST':
            if request.form.get('action') == "SaveNote":
                user.create_ticket_reply(request.form["reply-text"], None, g.current_user, ticketid, isNote=True)
            else:
                user.create_ticket_reply(request.form["reply-text"], None, g.current_user, ticketid)
            return redirect(url_for('viewTicket', ticketid = ticketid))
        return redirect(url_for('viewTicket', ticketid = ticketid))
    else:
        abort(403)


# the about page. this shows the current software version and some general information about SimpleTicket.
@app.route('/about')
def about():
    return render_template('about.html')

# the login page. this allows a user to authenticate to enable them to create and edit tickets.
@app.route('/login', methods=['GET', 'POST'])
def login(message = None):
    if request.method == 'POST':
        username = str.lower(request.form["login"]) # make sure the login string is only in lowercase
        password = request.form["password"]
        acc = user.verify_login(username, password)
        if acc:
            session['login'] = True
            session['acc_id'] = acc.id
            return redirect(url_for('home'))
        else: 
            message = lang["login-error"]
    return render_template('user-login.html', message = message)

# provide a logout url. we dont want users to get stuck logged in :)
@app.route('/logout')
def logout():
    session['login'] = False
    session['acc_id'] = None
    return redirect(url_for('home'))

# the password reset page to enable the users to reset their own password, provided they know their own email address.
@app.route('/pwreset', methods=['GET', 'POST'])
def resetPW():
    message = None
    if request.method == 'POST':
        message = lang['password-reset-form-message']
        userobj = m.User.query.filter_by(email = request.form["email"]).first()
        if userobj == None:
            message = lang['user-not-found-error']
            return render_template('user-password-reset.html', message = message)
        user.resetpw(userobj)
        return render_template('user-password-reset.html', message = message)
    return render_template('user-password-reset.html', message = message)

@app.route('/add-admin', methods=['GET', 'POST'])
def addAdmin():
    if os.path.exists(config.CREATE_ADMIN_FILE):
        if request.method == 'POST':
            try:
                user.create_user(str.lower(request.form["username"]), request.form["fullname"], request.form["email"], user.hashPassword(request.form["password"]), highPermissionLevel=True)
            except sqlalchemy.exc.IntegrityError:
                return render_template('user-signup.html', perms = lang["high-perms"], message = lang["user-create-error"])
            return redirect(url_for('login'))
        return render_template('user-signup.html', perms = lang["high-perms"])
    else:
        abort(403)

@app.route('/add-user', methods=['GET', 'POST'])
def addUser():
    if "login" in session.keys() and session['login'] and g.current_user.highPermissionLevel:
        if request.method == 'POST':
            try:
                user.create_user(str.lower(request.form["username"]), request.form["fullname"], request.form["email"], user.hashPassword(request.form["password"]), highPermissionLevel=False)
            except sqlalchemy.exc.IntegrityError:
                return render_template('user-signup.html', perms = lang["low-perms"], message = lang["user-create-error"])
            return redirect(url_for('login'))
        return render_template('user-signup.html', perms = lang["low-perms"])
    else:
        abort(403)

@app.route('/account-settings', methods=['GET', 'POST'])
def changeSettings():
    if "login" in session.keys() and session['login']:
        if request.method == 'POST':
            try:
                user.modify_user_password(g.current_user.id, user.hashPassword(request.form["password"]))
            except sqlalchemy.exc.IntegrityError:
                return render_template('account-settings.html', message = lang["user-modify-error"])
            return redirect(url_for('home'))
        return render_template('account-settings.html')
    else:
        abort(403)

@app.route('/admin-settings', methods=['GET', 'POST'])
def adminUserSettigs():
    if "login" in session.keys() and session['login'] and g.current_user.highPermissionLevel:
        if request.method == 'POST':
            try:
                user.modify_user_password(user.get_userid(request.form["username"]), user.hashPassword(request.form["password"]))
            except sqlalchemy.exc.IntegrityError:
                return render_template('admin-settings.html', message = lang["user-modify-error"])
            return redirect(url_for('home'))
        return render_template('admin-settings.html')
    else:
        abort(403)