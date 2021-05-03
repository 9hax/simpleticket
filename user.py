import bcrypt
import config
import smtpconfig
import json
import time
import datetime
import random
import string
from simpleticket import m

# prepare language files

with open("lang/"+config.LANGUAGE+".json",'r',encoding="utf-8") as langfile:
    lang = json.load(langfile)

def resetpw(user):
    newPassword = ''.join(random.choices(string.ascii_uppercase + string.digits, k = random.randint(20,30)))
    user.password = hashPassword(newPassword)
    m.db.session.commit()   
    sendmail(user.email, lang["password-reset-mail"].replace("%PW%", newPassword), lang["password-reset"]+" | "+config.SITE_NAME)
    del(newPassword)

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

def create_ticket_reply(text, media, created_by, main_ticket_id, isNote = False):
    new_ticket = m.TicketReply()
    new_ticket.text = text
    new_ticket.media = media
    new_ticket.isNote = isNote
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
    

def sendmail(address, htmlcontent, subject):
    import smtplib, ssl
    mailstring = "From: "+smtpconfig.SMTP_USER+"\nTo: "+address+"\nSubject: "+subject+"\n\n"+htmlcontent+"\n"
    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtpconfig.SMTP_SERVER, smtpconfig.SMTP_PORT, context=ssl_context) as smtpserver:
        smtpserver.login(smtpconfig.SMTP_USER, smtpconfig.SMTP_PASSWORD)
        smtpserver.sendmail(smtpconfig.SMTP_USER, address, mailstring)

def getTime(timestamp):
    try:
        return datetime.datetime.fromtimestamp(timestamp).strftime(config.TIMEFORMAT)
    except:
        return "Invalid time"

def hasValidReply(ticketid):
    ticketReplyList = m.TicketReply.query.filter_by(main_ticket_id = ticketid).all()
    for reply in ticketReplyList:
        if m.User.query.filter_by(id = reply.created_by_id).first().highPermissionLevel:
            return True
    return False