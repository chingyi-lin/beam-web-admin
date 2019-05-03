from app import db

class Activity(db.Model):
    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    login_timestamp = db.Column(db.Date, unique=False, nullable=False, server_default=db.func.now())
    location = db.Column(db.String(100), unique=False, nullable=False)
    shared_url_id = db.Column(db.Integer, db.ForeignKey('shared_url.id'), nullable=False)

    def __init__(location, shared_url_id, id=None):
        self.location = location
        self.shared_url_id  = shared_url_id 
