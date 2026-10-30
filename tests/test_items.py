from studentsync.db import get_db


def item_id(app, title):
    with app.app_context():
        return get_db().execute("SELECT id FROM items WHERE title = ?", (title,)).fetchone()["id"]


def test_create_edit_delete(actions, app, client):
    actions.register()
    res = actions.add_item(title="Bio lab report")
    html = res.get_data(as_text=True)
    assert "Bio lab report" in html and "11:59 PM" in html

    iid = item_id(app, "Bio lab report")
    res = actions.post(f"/items/{iid}/edit", {
        "title": "Bio lab report v2", "description": "", "item_type": "event",
        "due_date": "2030-06-02", "due_time": "",
    }, token_path=f"/items/{iid}/edit")
    html = res.get_data(as_text=True)
    assert "Bio lab report v2" in html and "Jun 2, 2030" in html

    res = actions.post(f"/items/{iid}/delete", {}, token_path="/dashboard")
    assert "Bio lab report v2" not in res.get_data(as_text=True).split("deleted")[-1]
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0


def test_item_validation(actions):
    actions.register()
    html = actions.add_item(title="", due_date="not-a-date", item_type="bogus").get_data(as_text=True)
    assert "Title is required" in html
    assert "valid date" in html
    assert "Assignment or Event" in html


def test_items_persist_across_sessions(actions, client):
    actions.register()
    actions.add_item(title="Midterm")
    actions.logout()
    assert "Midterm" in actions.login().get_data(as_text=True)


def test_users_only_see_and_modify_their_own_items(actions, app, client):
    actions.register(email="a@example.edu", name="Alice")
    actions.add_item(title="Alice secret")
    actions.logout()

    actions.register(email="b@example.edu", name="Bob")
    assert "Alice secret" not in client.get("/dashboard").get_data(as_text=True)

    iid = item_id(app, "Alice secret")
    assert client.get(f"/items/{iid}/edit").status_code == 404
    res = actions.post(f"/items/{iid}/delete", {}, follow=False, token_path="/dashboard")
    assert res.status_code == 404
    res = actions.post(f"/items/{iid}/edit", {
        "title": "hacked", "item_type": "event", "due_date": "2030-01-01",
    }, follow=False, token_path="/dashboard")
    assert res.status_code == 404
    with app.app_context():
        assert get_db().execute("SELECT title FROM items WHERE id = ?", (iid,)).fetchone()["title"] == "Alice secret"


def test_filter_by_type(actions, client):
    actions.register()
    actions.add_item(title="HW 1", item_type="assignment")
    actions.add_item(title="Club meeting", item_type="event")
    html = client.get("/dashboard?type=event").get_data(as_text=True)
    assert "Club meeting" in html and "HW 1" not in html
