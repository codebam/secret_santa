import os
from flask import Flask
from secret_santa import db, auth, index, account, signup, mylist, admin, match


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "secret_santa.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    # initialize the database

    app.register_blueprint(index.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(signup.bp)
    app.register_blueprint(mylist.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(match.bp)
    # register the blueprints from the factory

    return app
