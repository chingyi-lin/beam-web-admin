from app import db

class Note(db.Model):
    # __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=False, nullable=False)
    content = db.Column(db.String(200), unique=False, nullable=False)
    category = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_note = db.relationship("SharedNote", backref="user")

    def __init__(self, title, content, category, user_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.user_id = user_id

    def __repr__(self):
        return '<Note %r>' % (self.title)

    def __eq__(self, other):
        return int(self.id) == int(other.id)
