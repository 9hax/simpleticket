from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(400), unique=True, nullable=False)
    fullname = db.Column(db.Text, unique=False, nullable=True)
    email = db.Column(db.String(400), unique=True, nullable=True)
    password = db.Column(db.String(1000), unique=False, nullable=True)
    passwordResetTimer = db.Column(db.Integer, unique=False, nullable=True, default=-1)
    highPermissionLevel = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    def __repr__(self):
        return '<User %r>' % self.username

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), unique=False, nullable=True)
    is_open = db.Column(db.Boolean, unique=False, nullable = False, default= True)
    text = db.Column(db.Text, unique=False, nullable=False)
    media = db.Column(db.Text, unique=False, nullable=True) #This contains base64'ed binary images and videos in a python list.
    time = db.Column(db.Integer, unique = False) # The time the ticket was created in epoch seconds
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_by = db.relationship('User', backref='tickets_created_by', foreign_keys=[created_by_id])
    assigned_to = db.relationship('User', backref='tickets_assigned_to', foreign_keys=[assigned_to_id])
    def __repr__(self):
        return '<Ticket %r>' % self.title

class TicketReply(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, unique=False, nullable=False)
    media = db.Column(db.Text, unique=False, nullable=True)
    time = db.Column(db.Integer, unique = False) # The time the ticket reply was created in epoch seconds
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    main_ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))

    created_by = db.relationship('User', backref='ticket_reply_by', foreign_keys=[created_by_id])
    main_ticket = db.relationship('Ticket', backref = 'ticket_reply_main_ticket', foreign_keys=[main_ticket_id])
    def __repr__(self):
        return '<TicketReply to %r>' % self.main_ticket