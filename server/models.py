from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for the many-to-many Session↔Speaker relationship
session_speakers = db.Table(
    'session_speakers',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.id'), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String,  nullable=False)
    location = db.Column(db.String)
    # One-to-many → if an Event is deleted, its Sessions are deleted too
    sessions = db.relationship('Session', back_populates='event', cascade='all, delete')

    def __repr__(self):
        return f"<Event id={self.id} name={self.name!r}>"

class Session(db.Model):
    __tablename__ = 'sessions'
    id         = db.Column(db.Integer,   primary_key=True)
    title      = db.Column(db.String,    nullable=False)
    start_time = db.Column(db.DateTime)
    event_id   = db.Column(db.Integer,   db.ForeignKey('events.id'))
    # backref to Event
    event      = db.relationship('Event', back_populates='sessions')
    # many-to-many with Speaker
    speakers   = db.relationship('Speaker', secondary=session_speakers, back_populates='sessions')

    def __repr__(self):
        return f"<Session id={self.id} title={self.title!r}>"

class Speaker(db.Model):
    __tablename__ = 'speakers'
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String,  nullable=False)
    # one-to-one → if a Speaker is deleted, their Bio is deleted
    bio      = db.relationship('Bio', back_populates='speaker', uselist=False, cascade='all, delete')
    # many-to-many with Session
    sessions = db.relationship('Session', secondary=session_speakers, back_populates='speakers')

    def __repr__(self):
        return f"<Speaker id={self.id} name={self.name!r}>"

class Bio(db.Model):
    __tablename__ = 'bios'
    id         = db.Column(db.Integer, primary_key=True)
    bio_text   = db.Column(db.String)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))
    # backref to Speaker
    speaker    = db.relationship('Speaker', back_populates='bio')

    def __repr__(self):
        return f"<Bio id={self.id} speaker_id={self.speaker_id}>"