import bcrypt
import config
import smtpconfig
import json
import time
import datetime
from simpleticket import m

# prepare language files

with open("lang/"+config.LANGUAGE+".json",'r',encoding="utf-8") as langfile:
    lang = json.load(langfile)

def resetpw(email):
    sendmail(email, "Place an email text here.")

def verify_login(u, p):
    potential_user = m.User.query.filter_by(username=u.lower()).first()
    if potential_user:
        if bcrypt.checkpw(p.encode('utf-8'), potential_user.password.encode('utf-8')):
            return potential_user

    return False

def hashPassword(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode()

def get_userid(username):
    return m.User.query.filter_by(username = username).first().id

def get_user(userid):
    return m.User.query.get(userid)

def create_ticket(title, text, media, created_by, assigned_to):
    new_ticket = m.Ticket()
    new_ticket.title = title
    new_ticket.is_open = True
    new_ticket.text = text
    new_ticket.media = media
    new_ticket.time = time.time()
    new_ticket.created_by = created_by
    new_ticket.assigned_to = assigned_to
    m.db.session.add(new_ticket)
    m.db.session.commit()

def create_ticket_reply(text, media, created_by, main_ticket_id):
    new_ticket = m.TicketReply()
    new_ticket.text = text
    new_ticket.media = media
    new_ticket.time = time.time()
    new_ticket.created_by = created_by
    new_ticket.main_ticket_id = main_ticket_id
    m.db.session.add(new_ticket)
    m.db.session.commit()

def create_user(username, fullname, email, hashedPassword, passwordResetTimer = -1, highPermissionLevel = 0):
    new_user = m.User()
    new_user.username = username.lower()
    new_user.fullname = fullname
    new_user.email = email
    new_user.password = hashedPassword
    new_user.passwordResetTimer = passwordResetTimer
    new_user.highPermissionLevel = highPermissionLevel
    m.db.session.add(new_user)
    m.db.session.commit()

def modify_user_password(userid, newPasswordHash):
    modified_user = get_user(userid)
    modified_user.password = newPasswordHash
    m.db.session.commit()
    

def sendmail(address, htmlcontent):
    import smtplib, ssl
    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpconfig.SMTP_SERVER, smtpconfig.SMTP_PORT, context=ssl_context) as smtpserver:
        smtpserver.login(smtpconfig.SMTP_USER, smtpconfig.SMTP_PASSWORD)
        smtpserver.sendmail(smtpconfig.SMTP_USER, address, htmlcontent)

def getTime(timestamp):
    try:
        return datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M:%S, %m.%d.%Y")
    except:
        return "Invalid time"