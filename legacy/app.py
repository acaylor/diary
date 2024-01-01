import sqlite3
import logging
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


# Helper function to connect to a SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    logging.debug("Opening connection to database")
    return conn


# helper function to retrieve a row in the database
def get_entry(entry_id):
    conn = get_db_connection()
    # Retrieve an entry by primary key 'id'
    entry = conn.execute('SELECT * FROM entry WHERE id = ?',
                         (entry_id,)).fetchone()
    conn.close()
    logging.debug("Closing connection to database")
    if entry is None:
        logging.error("Error: no entry returned")
        # imported a function to return 404 if there is no result
        abort(404)
    return entry


app = Flask(__name__)
# Check flask documentation for secret key usage in sessions
# This will be used to only allow users with the key to make an entry
# This should not be stored in source code, use an env var
app.config['SECRET_KEY'] = '4jksdFGQWEAL4sgqwfv36sdwsg231weATGHY'


@app.route('/')
def index():  # put application's code here
    conn = get_db_connection()
    entries = conn.execute('SELECT * FROM entry').fetchall()
    conn.close()
    logging.debug("Closing connection to database")

    return render_template('index.html', entries=entries)


@app.route('/<int:entry_id>')
def entry(entry_id):
    entry = get_entry(entry_id)
    return render_template('entry.html', entry=entry)


@app.route('/create', methods=('GET', 'POST'))
# function to create a new post when a user makes a POST request to the /create route
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO entry (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            logging.debug("Closing connection to database")
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
# function to edit a post when a user makes a POST request to the route
def edit(id):
    entry = get_entry(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE entry SET title = ?, content = ?'
                         'WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            logging.debug("Closing connection to database")
            return redirect(url_for('index'))

    return render_template('edit.html', entry=entry)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    entry = get_entry(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM entry WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{} was deleted!'.format(entry['title']))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
