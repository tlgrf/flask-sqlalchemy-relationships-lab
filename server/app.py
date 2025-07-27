from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Event, Session, Speaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
Migrate(app, db)

# 1. GET /events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    payload = [{'id': e.id, 'name': e.name, 'location': e.location} for e in events]
    return jsonify(payload), 200

# 2. GET /events/<id>/sessions
@app.route('/events/<int:id>/sessions', methods=['GET'])
def get_event_sessions(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    payload = [{
        'id':     s.id,
        'title':  s.title,
        'start_time': s.start_time.isoformat() if s.start_time else None
    } for s in event.sessions]
    return jsonify(payload), 200

# 3. GET /speakers
@app.route('/speakers', methods=['GET'])
def get_speakers():
    speakers = Speaker.query.all()
    payload = [{'id': s.id, 'name': s.name} for s in speakers]
    return jsonify(payload), 200

# 4. GET /speakers/<id>
@app.route('/speakers/<int:id>', methods=['GET'])
def get_speaker(id):
    sp = Speaker.query.get(id)
    if not sp:
        return jsonify({'error': 'Speaker not found'}), 404
    bio_text = sp.bio.bio_text if sp.bio else 'No bio available'
    return jsonify({'id': sp.id, 'name': sp.name, 'bio_text': bio_text}), 200

# 5. GET /sessions/<id>/speakers
@app.route('/sessions/<int:id>/speakers', methods=['GET'])
def get_session_speakers(id):
    sess = Session.query.get(id)
    if not sess:
        return jsonify({'error': 'Session not found'}), 404
    payload = []
    for sp in sess.speakers:
        bio_text = sp.bio.bio_text if sp.bio else 'No bio available'
        payload.append({'id': sp.id, 'name': sp.name, 'bio_text': bio_text})
    return jsonify(payload), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555)