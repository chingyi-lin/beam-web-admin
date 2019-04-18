from flask import render_template, redirect, request, url_for, flash, json
from app import app, models, login_manager, db, user
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *
from .user import User
from .forms import LoginForm, SignUpForm, NoteForm

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', username = current_user.username)
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

@app.route('/note', methods=['GET', 'POST'])
def addNote():
    form = NoteForm()
    # if form.validate_on_submit():
    #     noteTitle = form.noteTitle.data
    #     noteContent = form.noteContent.data
    #     # newUser = User(username, email, nickname, contact_no)
    #     # newUser.set_password(password)
    #     # addToDatabase(newUser)
    #     # login_user(newUser)
    #     return redirect(url_for('index'))
    return render_template('notes.html', title = "Add Secure Note", form = form, username = "Guest")

@app.route('/share', methods=['GET', 'POST'])
def share():
    # form = NoteForm()
    # if form.validate_on_submit():
    #     noteTitle = form.noteTitle.data
    #     noteContent = form.noteContent.data
    #     # newUser = User(username, email, nickname, contact_no)
    #     # newUser.set_password(password)
    #     # addToDatabase(newUser)
    #     # login_user(newUser)
    #     return redirect(url_for('index'))
    return render_template('share.html', title = "Share", username = "Guest")