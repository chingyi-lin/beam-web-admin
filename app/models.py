from app import app, login_manager, user, db, note, shared_note, account, shared_url, activity
from flask_login import UserMixin, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .user import User
from .note import Note
from .shared_note import SharedNote
from .account import Account
from .shared_url import SharedURL
from .activity import Activity


# --- Database API ---

def addToDatabase(newObject):
    db.session.add(newObject)
    db.session.commit()
    return 

def getUserByUsername(query):
    return User.query.filter_by(username=query).first()

def getAllNoteByUserID(query):
    return Note.query.filter_by(user_id=query).all()

def getNoteByNoteID(query):
    return Note.query.filter_by(id=query).first()

def getAllSharedNoteByNoteID(query):
    return SharedNote.query.filter_by(note_id=query).all()

def getAllNoteByUserID(query):
    return Account.query.filter_by(user_id=query).all()

def getAccountByNoteID(query):
    return Account.query.filter_by(id=query).first()

def getAllSharedURLByAccountID(query):
    return SharedURL.query.filter_by(account_id=query).all()

def getAllActivityBySharedURLID(query):
    return Activity.query.filter_by(shared_url_id=query).all()

# --- Login/Sign Up Helper Methods ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def isUsernameUsed(username):
    user = User.query.filter_by(username=username).first()
    return False if user is None else True
    
def isEmailUsed(email):
    user = User.query.filter_by(email=email).first()
    return False if user is None else True
    
def validateLogin(username, password):
    comparedUser = getUserByUsername(username)
    if comparedUser is None or not check_password_hash(comparedUser.password_hash, password):
        return False
    login_user(comparedUser)
    return True