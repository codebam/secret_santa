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
from secret_santa.db import get_db
from secret_santa.auth import login_required

bp = Blueprint("signup", __name__, url_prefix="/signup")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        db = get_db()
        error = None
        terms = None

        try:
            terms = request.form["terms"]
        except:
            error = "Must accept terms and conditions to continue."
            terms = None

        if error is None:
            if terms is not None:
                db.execute("UPDATE user SET terms = ? WHERE id = ?", (1, g.user["id"]))
                db.commit()

            return redirect(url_for("index.index"))

        flash(error)

    return render_template("signup.html")
