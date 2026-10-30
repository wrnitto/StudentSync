import secrets

from flask import abort, request, session


def get_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


def init_app(app):
    app.jinja_env.globals["csrf_token"] = get_token

    @app.before_request
    def check_csrf():
        if app.config.get("TESTING_DISABLE_CSRF"):
            return
        if request.method == "POST":
            sent = request.form.get("csrf_token", "")
            if not sent or not secrets.compare_digest(sent, session.get("csrf_token", "")):
                abort(400, description="Invalid or missing form token. Please reload the page and try again.")
