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

bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("/", methods=("GET",))
def index():
    match = (
        get_db()
        .execute("SELECT * FROM user WHERE id = ?", (g.user["match"],))
        .fetchone()
    )

    return render_template("match/index.html", match=match)
