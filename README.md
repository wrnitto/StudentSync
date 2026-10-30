# StudentSync

StudentSync is a mobile-friendly web application that helps college students organize schoolwork and personal responsibilities in one place.

## Prototype 1 scope

- Create an account and log in with email + password (passwords are hashed)
- Log out
- Dashboard listing your assignments and events (upcoming and past), with an All / Assignments / Events filter
- Add, edit, and delete assignments and events (title, description, type, date, optional time)
- Data is saved in a SQLite database; each user only sees and can change their own items
- Responsive layout for desktop and mobile browsers

Not in this prototype: LMS importing, grades, instructor/employer accounts, shared calendars, messaging, payments, automatic scheduling, or conflict resolution.

## Tech stack

- Python 3.10+ with [Flask](https://flask.palletsprojects.com/)
- SQLite (Python's built-in `sqlite3`)
- Server-rendered Jinja templates and plain CSS (no build step)

## Project structure

```
app.py                      # entry point (python app.py)
requirements.txt
studentsync/
  __init__.py               # app factory, registers blueprints
  db.py                     # SQLite connection + schema setup
  schema.sql                # users and items tables
  auth.py                   # register, login, logout, login_required
  items.py                  # dashboard and assignment/event CRUD
  csrf.py                   # simple CSRF protection for forms
  templates/                # Jinja templates (base, auth/, items/)
  static/style.css          # responsive styles
tests/                      # pytest tests
```

New features can be added as new blueprints (e.g. `studentsync/calendar.py`) and new tables in `schema.sql`.

## Running locally

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. To try it from a phone on the same Wi-Fi, open `http://<your-computer-ip>:5000`.

The database is created automatically at `instance/studentsync.sqlite`. Delete that file to start over.

For anything beyond local development, set a real secret key:

```bash
export SECRET_KEY="some-long-random-string"
```

## Running tests

```bash
pytest
```
