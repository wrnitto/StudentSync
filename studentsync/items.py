from datetime import date, datetime

from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from .auth import login_required
from .db import get_db

bp = Blueprint("items", __name__)

ITEM_TYPES = {"assignment": "Assignment", "event": "Event"}


def get_owned_item(item_id):
    item = get_db().execute(
        "SELECT * FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"])
    ).fetchone()
    if item is None:
        abort(404)
    return item


def parse_item_form(form):
    data = {
        "title": form.get("title", "").strip(),
        "description": form.get("description", "").strip(),
        "item_type": form.get("item_type", ""),
        "due_date": form.get("due_date", "").strip(),
        "due_time": form.get("due_time", "").strip(),
    }
    errors = []
    if not data["title"]:
        errors.append("Title is required.")
    elif len(data["title"]) > 200:
        errors.append("Title must be 200 characters or fewer.")
    if data["item_type"] not in ITEM_TYPES:
        errors.append("Please choose Assignment or Event.")
    try:
        date.fromisoformat(data["due_date"])
    except ValueError:
        errors.append("Please enter a valid date.")
    if data["due_time"]:
        try:
            datetime.strptime(data["due_time"], "%H:%M")
        except ValueError:
            errors.append("Please enter a valid time.")
    return data, errors


def format_item(row):
    item = dict(row)
    d = date.fromisoformat(item["due_date"])
    item["date_display"] = d.strftime("%a, %b %-d, %Y")
    if item["due_time"]:
        item["time_display"] = datetime.strptime(item["due_time"], "%H:%M").strftime("%-I:%M %p")
        due = datetime.combine(d, datetime.strptime(item["due_time"], "%H:%M").time())
        item["is_past"] = due < datetime.now()
    else:
        item["time_display"] = None
        item["is_past"] = d < date.today()
    item["type_label"] = ITEM_TYPES[item["item_type"]]
    return item


@bp.route("/dashboard")
@login_required
def dashboard():
    type_filter = request.args.get("type", "all")
    query = "SELECT * FROM items WHERE user_id = ?"
    params = [g.user["id"]]
    if type_filter in ITEM_TYPES:
        query += " AND item_type = ?"
        params.append(type_filter)
    else:
        type_filter = "all"
    query += " ORDER BY due_date, due_time IS NULL, due_time, id"

    items = [format_item(r) for r in get_db().execute(query, params).fetchall()]
    upcoming = [i for i in items if not i["is_past"]]
    past = [i for i in items if i["is_past"]]
    return render_template(
        "items/dashboard.html",
        upcoming=upcoming,
        past=past,
        type_filter=type_filter,
        item_types=ITEM_TYPES,
        form={"item_type": "assignment"},
    )


@bp.route("/items/new", methods=("GET", "POST"))
@login_required
def create():
    form = {"item_type": request.args.get("type", "assignment")}
    if request.method == "POST":
        form, errors = parse_item_form(request.form)
        if not errors:
            db = get_db()
            db.execute(
                "INSERT INTO items (user_id, title, description, item_type, due_date, due_time)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                (g.user["id"], form["title"], form["description"], form["item_type"],
                 form["due_date"], form["due_time"] or None),
            )
            db.commit()
            flash(f"{ITEM_TYPES[form['item_type']]} \"{form['title']}\" added.", "success")
            return redirect(url_for("items.dashboard"))
        for e in errors:
            flash(e, "error")
    return render_template("items/form.html", form=form, item=None, item_types=ITEM_TYPES)


@bp.route("/items/<int:item_id>/edit", methods=("GET", "POST"))
@login_required
def edit(item_id):
    item = get_owned_item(item_id)
    form = dict(item)
    if request.method == "POST":
        form, errors = parse_item_form(request.form)
        if not errors:
            db = get_db()
            db.execute(
                "UPDATE items SET title = ?, description = ?, item_type = ?, due_date = ?, due_time = ?,"
                " updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
                (form["title"], form["description"], form["item_type"], form["due_date"],
                 form["due_time"] or None, item_id, g.user["id"]),
            )
            db.commit()
            flash(f"\"{form['title']}\" updated.", "success")
            return redirect(url_for("items.dashboard"))
        for e in errors:
            flash(e, "error")
    return render_template("items/form.html", form=form, item=item, item_types=ITEM_TYPES)


@bp.route("/items/<int:item_id>/delete", methods=("POST",))
@login_required
def delete(item_id):
    item = get_owned_item(item_id)
    db = get_db()
    db.execute("DELETE FROM items WHERE id = ? AND user_id = ?", (item_id, g.user["id"]))
    db.commit()
    flash(f"\"{item['title']}\" deleted.", "success")
    return redirect(url_for("items.dashboard"))
