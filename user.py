from simpleticket import m
import bcrypt
import smtpconfig
import json

# prepare language files

with open("lang/"+config.LANGUAGE+".json",'r',encoding="utf-8") as langfile:
    lang = json.load(langfile)

def resetpw(email):
    sendmail(email, "Place an email text here.")

def verify_login(u, p):
    potential_user = m.User.query.filter_by(username=u).first()
    if potential_user:
        if bcrypt.checkpw(p.encode('utf-8'), potential_user.password.encode('utf-8')):
            return potential_user

    return False

def hashPassword(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12)).decode()

def get_user(id):
    return m.User.query.get(id)

def create_user(username, email, hashedPassword, passwordResetTimer = -1, highPermissionLevel = 0):
    new_user = m.User()
    new_user.username = username
    new_user.email = email
    new_user.password = hashedPassword
    new_user.passwordResetTimer = passwordResetTimer
    new_user.highPermissionLevel = highPermissionLevel
    m.db.session.add(new_user)
    m.db.session.commit()

def sendmail(address, htmlcontent):
    import smtplib, ssl
    sslContext = ssl.create_default_context()
    with smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, context=sslContext) as smtpserver:
        smtpserver.login(config.SMTP_USER, config.SMTP_PASSWORD)
        smtpserver.sendmail(config.SMTP_USER, address, htmlcontent)