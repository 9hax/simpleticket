from flask_sqlalchemy import *
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(400), unique=True, nullable=False)
    email = db.Column(db.String(400), unique=True, nullable=True)
    password = db.Column(db.String(1000), unique=False, nullable=True)
    passwordResetTimer = db.Column(db.Integer, unique=False, nullable=True, default=-1)
    highPermissionLevel = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    def __repr__(self):
        return '<User> %r' % self.username

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), unique=False, nullable=True)
    text = db.Column(db.Text, unique=False, nullable=False)
    media = db.Column(db.Text, unique=False, nullable=True) #This contains base64'ed binary images and videos in a python list.
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_by = db.relationship('User', backref='tickets_created_by', foreign_keys=[created_by_id])
    assigned_to = db.relationship('User', backref='tickets_assigned_to', foreign_keys=[assigned_to_id])
