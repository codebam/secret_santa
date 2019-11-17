import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from secret_santa.db import get_db
from secret_santa.auth import login_required

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        username = request.form["username"]
        password = request.form["password"]
        new_password = request.form["new_password"]
        db = get_db()
        error = None

        if not password:
            error = "Password is required to update account info."
        elif not check_password_hash(g.user["password"], password):
            error = "Incorrect password."
        # user must enter their password to update info

        if error is None:
            if name:
                db.execute(
                    "UPDATE user SET name = ? WHERE id = ?", (name, g.user["id"])
                )

            if surname:
                db.execute(
                    "UPDATE user SET surname = ? WHERE id = ?", (surname, g.user["id"])
                )

            if username:
                db.execute(
                    "UPDATE user SET username = ? WHERE id = ?",
                    (username, g.user["id"]),
                )

            if new_password:
                db.execute(
                    "UPDATE user SET password = ? WHERE id = ?",
                    (generate_password_hash(new_password), g.user["id"]),
                )
            db.commit()

            return redirect(url_for("account.index"))

        flash(error)

    return render_template("account/index.html")
