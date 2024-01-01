import os

from flask import Flask

def create_app(test_config=None):
    # create and configure flask app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'diary.sqlite'),
    )

    if test_config is None:
        # load the config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed
        app.config.from_mapping(test_config)
    
    # ensure dir exists on filesystem
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import the db instance from db.py
    from . import db
    db.init_app(app)

    # import and register the auth instance from auth.py
    from . import auth
    app.register_blueprint(auth.bp)

    # import the diary instance from diary.py
    from . import diary
    app.register_blueprint(diary.bp)
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello there.'
    
    return app
