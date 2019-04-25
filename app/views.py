from flask import render_template, redirect, request, url_for, flash, json
from app import app, models, login_manager, db, user, note, shared_note
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .user import User
from .note import Note
from .forms import LoginForm, SignUpForm, NoteForm
from .shared_note import SharedNote

@app.route('/')
def index():
    if current_user.is_authenticated:
        notes = getAllNoteByUserID(current_user.id)
        return render_template('index.html', username = current_user.username, notes=notes)
    else:
        return render_template('index.html', username = "Guest")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        nickname = form.nickname.data
        contact_no = form.phone.data
        if isUsernameUsed(username) is True:
            # in this case user with this username exists already
            flash("Username is already used. Please pick a different one.")
            return render_template('signup.html', title = "Sign Up", form = form)
        if isEmailUsed(email) is True:
            # in this case user with this username exists already
            flash("Email is already used. Please pick a different one.")
            return render_template('signup.html', title = "Sign Up", form = form)
        # in case it does not exist
        newUser = User(username, email, nickname, contact_no)
        newUser.set_password(password)
        addToDatabase(newUser)
        login_user(newUser)
        return redirect(url_for('index'))
    return render_template('signup.html', title = "Sign Up", form = form, username = "Guest")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if validateLogin(username, password):
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', title = 'Log In', form = form, username = "Guest")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

# TODO: Category drop down. Now it's hard coded "default_category"
@app.route('/note', methods=['GET', 'POST'])
@login_required
def addNote():
    form = NoteForm()
    if form.validate_on_submit():
        noteTitle = form.noteTitle.data
        noteContent = form.noteContent.data
        newNote = Note(noteTitle, noteContent, "default_category", current_user.id)
        addToDatabase(newNote)
        return redirect(url_for('share', note_id=newNote.id, request_from="adding"))
    return render_template('notes.html', title = "Add Secure Note", form = form, username = current_user.username)

@app.route('/note/<int:note_id>')
@login_required
def viewNote(note_id):
    note = getNoteByNoteID(note_id)
    shared_notes = getAllSharedNoteByNoteID(note_id)
    return render_template('entry-note.html', note=note, shared_notes=shared_notes)

@app.route('/share/<int:note_id>/<request_from>')
@login_required
def share(note_id, request_from):
    return render_template('share.html', title="Share", username=current_user.username, note_id=note_id, request_from=request_from)

@app.route('/share-submit/<int:note_id>/<string:request_from>', methods=['POST'])
def shareSubmit(note_id, request_from):
    duration = request.form['duration']
    newSharedNote = SharedNote(duration, note_id)
    addToDatabase(newSharedNote)
    newSharedNote.set_magiclink()
    db.session.commit()
    return render_template('confirm.html', title = "Sharing Complete", username = current_user.username, magiclink=newSharedNote.magiclink, note_id=note_id, request_from=request_from)

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    return render_template('entry.html', title = "Entry")
