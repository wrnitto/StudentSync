def test_register_logs_in_and_shows_dashboard(actions):
    res = actions.register()
    assert res.request.path == "/dashboard"
    assert "Hi, Sam" in res.get_data(as_text=True)


def test_duplicate_email_rejected(actions):
    actions.register()
    actions.logout()
    res = actions.register(email="SAM@example.edu")
    assert "already exists" in res.get_data(as_text=True)


def test_register_validation(actions):
    assert "at least 8" in actions.register(password="short").get_data(as_text=True)
    assert "valid email" in actions.register(email="nope").get_data(as_text=True)


def test_login_and_logout(actions, client):
    actions.register()
    actions.logout()
    assert client.get("/dashboard").status_code == 302

    bad = actions.login(password="wrongpassword")
    assert "Incorrect email or password" in bad.get_data(as_text=True)

    ok = actions.login()
    assert ok.request.path == "/dashboard"

    out = actions.logout()
    assert out.request.path == "/auth/login"
    assert client.get("/dashboard").status_code == 302


def test_password_is_hashed(actions, app):
    actions.register()
    from studentsync.db import get_db
    with app.app_context():
        row = get_db().execute("SELECT password_hash FROM users").fetchone()
    assert row["password_hash"] != "password123"


def test_post_without_csrf_rejected(client):
    res = client.post("/auth/login", data={"email": "a@b.co", "password": "x"})
    assert res.status_code == 400
