import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    app.teardown_appcontext(db.close_db)
    from pet_hotel.extentions import app_mysql
    app_mysql.init_app(app)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import booking
    app.register_blueprint(booking.bp)
    # app.add_url_rule('/booking', endpoint='index')

    # Pet
    from . import pet
    app.register_blueprint(pet.bp)
    app.add_url_rule('/pet', endpoint='index')

    # owner
    from . import owner
    app.register_blueprint(owner.bp)
    app.add_url_rule('/owner', endpoint='index')

    return app