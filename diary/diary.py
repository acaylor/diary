from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from diary.auth import login_required
from diary.db import get_db

bp = Blueprint('diary', __name__)

# show index of entries
@bp.route('/')
def index():
    db = get_db()
    entries = db.execute(
        'SELECT p.id, title, content, created, user_id, username'
        ' FROM entry p JOIN user u ON p.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('diary/index.html', entries=entries)

# route to create a new entry
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO entry (title, content, user_id)'
                ' VALUES (?, ?, ?)',
                (title, content, g.user['id'])
            )
            db.commit()
            return redirect(url_for('diary.index'))

    return render_template('diary/create.html')

# function to get an entry and return as dict
def get_entry(id, check_user=True):
    entry = get_db().execute(
        'SELECT p.id, title, content, created, user_id, username'
        '  FROM entry p JOIN user u ON p.user_id = u.id'
        '  WHERE p.id = ?',
        (id,)
    ).fetchone()

    if entry is None:
        abort(404, f"Entry id {id} does not exist.")

    if check_user and entry['user_id'] != g.user['id']:
        abort(403)
    
    return entry

# route to update existing entries
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    entry = get_entry(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE entry SET title = ?, content = ?'
                ' WHERE id = ?',
                (title, content, id)
            )
            db.commit()
            return redirect(url_for('diary.index'))

    return render_template('diary/update.html', entry=entry)

# Delete view is added to update page
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_entry(id)
    db = get_db()
    db.execute('DELETE FROM entry WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('diary.index'))

