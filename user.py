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