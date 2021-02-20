import os

from flask import Flask
from flask_mongoengine import MongoEngine
from cache import channelsCache


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if app.config["ENV"] == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    if app.config['SECRET_KEY'] is None:
        raise Exception(
            "SECRET_KEY can't be None. Try to generate one by command: python -c 'import os; print(os.urandom(16))', and copy the result into configs.py.")

    if app.config['OWNER_USER_ID'] is None:
        raise Exception(
            "OWNER_USER_ID can't be None. It is an integer user_id of your Clubhouse account, you can get it from token json file generated by OpenClubhouse-worker")

    @app.route("/alive")
    def alive():
        return {"alive": True}

    db = MongoEngine(app)
    channelsCache.init_cache(app.logger)

    # apply the blueprints to the app
    from handlers import clubhouse

    app.register_blueprint(clubhouse.bp)
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app
