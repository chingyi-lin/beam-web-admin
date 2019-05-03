from app import db
from hashids import Hashids

class SharedURL(db.Model):
    __tablename__ = "shared_url"

    id = db.Column(db.Integer, primary_key=True)
    magiclink = db.Column(db.String(100), unique=True, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    start_date = db.Column(db.DateTime, server_default=db.func.now())
    is_expired = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    activity = db.relationship("Activity", backref="shared_url")

    def __init__(self, duration, account_id, is_expired=False, id=None):
        self.id = id
        self.magiclink = ""
        self.duration = duration
        self.account_id = account_id
        self.is_expired = is_expired

    def set_magiclink(self):
        hashids = Hashids(salt='sAsd92$8s_|spc!!lm', min_length=8)
        print(self.id)
        self.magiclink = "https://www.beam.com/" + hashids.encode(int(self.id))

    def __repr__(self):
        return '<Shared Note %r>' % (self.title)

    def __eq__(self, other):
        return int(self.id) == int(other.id)
