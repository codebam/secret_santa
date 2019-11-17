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

bp = Blueprint("mylist", __name__, url_prefix="/mylist")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        mylist = request.form["mylist"]
        db = get_db()
        error = None

        if error is None:
            db.execute("UPDATE user SET list = ? WHERE id = ?", (mylist, g.user["id"]))
            db.commit()

            return redirect(url_for("mylist.index"))
        flash(error)

    return render_template("mylist/index.html")
