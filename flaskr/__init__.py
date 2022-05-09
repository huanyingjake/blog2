import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)  # load the instance config,if it exists, when not testing
    else:
        app.config.from_mapping(test_config)  # load the test config if passed in

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # asimple page that says hello
    @app.route('/hello')
    def hello():
        return 'hello worldsdffs'
    from . import db
    db.init_app(app)

    return app
