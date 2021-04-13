from simpleticket import m
import bcrypt
import config
import smtpconfig
import json

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

def get_user(id):
    return m.User.query.get(id)

def create_ticket(title, text, media, created_by, assigned_to):
    new_ticket = m.Ticket()
    new_ticket.title = title
    new_ticket.is_open = True
    new_ticket.text = text
    new_ticket.media = media
    new_ticket.created_by = created_by
    new_ticket.assigned_to = assigned_to
    m.db.session.add(new_ticket)
    m.db.session.commit()

def edit_ticket(current_ticket_id, new_open, new_assignee):
    current_ticket = m.Ticket.query.filter_by(id = current_ticket_id)
    current_ticket.is_open = new_open
    current_ticket.assigned_to = new_assignee
    m.db.session.commit()


def create_user(username, email, hashedPassword, passwordResetTimer = -1, highPermissionLevel = 0):
    new_user = m.User()
    new_user.username = username.loewr()
    new_user.email = email
    new_user.password = hashedPassword
    new_user.passwordResetTimer = passwordResetTimer
    new_user.highPermissionLevel = highPermissionLevel
    m.db.session.add(new_user)
    m.db.session.commit()

def sendmail(address, htmlcontent):
    import smtplib, ssl
    sslContext = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpconfig.SMTP_SERVER, smtpconfig.SMTP_PORT, context=sslContext) as smtpserver:
        smtpserver.login(smtpconfig.SMTP_USER, smtpconfig.SMTP_PASSWORD)
        smtpserver.sendmail(smtpconfig.SMTP_USER, address, htmlcontent)