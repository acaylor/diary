import sqlite3

import click

from flask import current_app, g

def get_db():
    # g is a special object for each request to db
    if 'db' not in g:
        # open a connection to the DATABASE config key
        g.db = sqlite3.connect(
            # current_app is a special object that points to flask app
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # return db rows as dicts
        g.db.row_factory = sqlite3.Row

    return g.db

# check if a connection was created and close if open
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# create a new database schema
def init_db():
    db = get_db()

    # open a file relative to the current package
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# define a cli command called init-db that calls init_db func
@click.command('init-db')
def init_db_command():
    # Clear existing data and create new tables
    init_db()
    click.echo('Initialized the database.')


# init a new app
def init_app(app):
    # flask call function when making requests to db
    app.teardown_appcontext(close_db)
    # add a new cli command that can be called with flask
    app.cli.add_command(init_db_command)