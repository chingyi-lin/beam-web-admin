from werkzeug.security import generate_password_hash
from app import db

class Account(db.Model):
    # __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    account_username = db.Column(db.String(20), unique=False, nullable=False)
    password_hash = db.Column(db.String(64), unique=False)
    website_name = db.Column(db.String(20), unique=False, nullable=False)
    website_url = db.Column(db.String(100), unique=False, nullable=False)
    category = db.Column(db.String(20), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_URL = db.relationship("SharedURL", backref="account")

    def __init__(self, account_username, website_name, website_url, category, user_id, id=None):
        self.id = id
        self.account_username = account_username
        self.website_name = website_name
        self.website_url = website_url
        self.category = category
        self.user_id = user_id
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<Note %r>' % (self.title)

    def __eq__(self, other):
        return int(self.id) == int(other.id)
