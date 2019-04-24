from app import db
from hashids import Hashids

class SharedNote(db.Model):
    # __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    magiclink = db.Column(db.String(100), unique=True, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    start_date = db.Column(db.DateTime, server_default=db.func.now())
    is_expired = db.Column(db.Boolean, nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)

    def __init__(self, duration, note_id, is_expired=False, id=None):
        self.id = id
        self.magiclink = ""
        self.duration = duration
        self.note_id = note_id
        self.is_expired = is_expired

    def set_magiclink(self):
        hashids = Hashids(salt='sAsd92$8s_|spc!!lm', min_length=8)
        print(self.id)
        self.magiclink = "https://www.beam.com/" + hashids.encode(int(self.id))

    def __repr__(self):
        return '<Shared Note %r>' % (self.title)

    def __eq__(self, other):
        return int(self.id) == int(other.id)
