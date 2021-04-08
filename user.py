from simpleticket import m
import bcrypt

def resetpw(kek):
    print(kek)

def verify_login(u, p):
    potential_user = m.User.query.filter_by(username=u).first()
    if potential_user:
        if bcrypt.checkpw(p.encode('utf-8'), potential_user.password.encode('utf-8')):
            return potential_user

    return False

def get_user(id):
    return m.User.query.get(id)

def create_user(username, email, password, passwordResetTimer = -1, highPermissionLevel = 0):
    new_user = m.User()
    new_user.username = username
    new_user.email = email
    new_user.password = password
    new_user.passwordResetTimer = passwordResetTimer
    new_user.highPermissionLevel = highPermissionLevel
    m.db.session.add(new_user)
    m.db.session.commit()