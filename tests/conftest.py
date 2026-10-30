import re

import pytest

from studentsync import create_app


@pytest.fixture
def app(tmp_path):
    return create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite")})


@pytest.fixture
def client(app):
    return app.test_client()


def csrf(client, path="/auth/login"):
    html = client.get(path, follow_redirects=True).get_data(as_text=True)
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


class Actions:
    def __init__(self, client):
        self.client = client

    def post(self, path, data, follow=True, token_path="/auth/login"):
        data = {"csrf_token": csrf(self.client, token_path), **data}
        return self.client.post(path, data=data, follow_redirects=follow)

    def register(self, email="sam@example.edu", password="password123", name="Sam"):
        return self.post("/auth/register", {
            "name": name, "email": email, "password": password, "confirm_password": password,
        }, token_path="/auth/register")

    def login(self, email="sam@example.edu", password="password123"):
        return self.post("/auth/login", {"email": email, "password": password})

    def logout(self):
        return self.post("/auth/logout", {}, token_path="/")

    def add_item(self, **overrides):
        data = {"title": "Essay", "description": "5 pages", "item_type": "assignment",
                "due_date": "2030-05-01", "due_time": "23:59", **overrides}
        return self.post("/items/new", data, token_path="/items/new")


@pytest.fixture
def actions(client):
    return Actions(client)
