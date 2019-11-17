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

bp = Blueprint("index", __name__, url_prefix="/")


@bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    return render_template("index.html")
