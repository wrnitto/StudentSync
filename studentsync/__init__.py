import os

from flask import Flask, redirect, session, url_for


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-change-me"),
        DATABASE=os.path.join(app.instance_path, "studentsync.sqlite"),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import auth, csrf, db, items

    db.init_app(app)
    csrf.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(items.bp)

    @app.route("/")
    def index():
        if session.get("user_id"):
            return redirect(url_for("items.dashboard"))
        return redirect(url_for("auth.login"))

    return app
