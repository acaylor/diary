import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from diary.db import get_db

# Create a new Blueprint obj named auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

# add route /register with the register view func
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # if the user submits data with the form the request will be POST
    if request.method == 'POST':
        # special dict for form key,value pairs
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # execute sql query with ? placeholder for user input
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                ) # only a hashed value of the password will be stored in the db
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        
        # if validation fails, show message to user
        flash(error)

    return render_template('auth/register.html')

# add route /login for login view func
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # return one row from the query or return None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        # hash the submitted password and compare to hash in db
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # session is dict that stores data across requests from a certain user
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# function that runs after view() for all routes
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

""" 
require login to view pages
return a view funct that wraps the original view
check if user is logged in or redirect
"""
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

