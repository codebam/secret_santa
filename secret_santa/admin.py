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

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user["id"] != 1:
            return redirect(url_for("index.index"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/", methods=("GET",))
@admin_required
def index():
    return render_template("admin/index.html")


@bp.route("/start", methods=("GET", "POST"))
@admin_required
def start():
    if request.method == "POST":
        db = get_db()
        confirm = None
        error = None

        try:
            confirm = request.form["confirm"]
        except:
            error = "You must confirm to perform this action."

        user_list = get_db().execute("SELECT * FROM user WHERE terms = 1").fetchall()

        if len(user_list) < 3:
            error = "You must have at least 3 participants to continue."

        if error is None:
            if confirm is not None:
                from random import shuffle

                shuffle(user_list)
                pairs = tuple(zip(user_list, user_list[1:] + user_list[:1]))

                for pair in pairs:
                    db.execute(
                        "UPDATE user SET match = ? WHERE id = ?",
                        (pair[1]["id"], pair[0]["id"]),
                    )
                db.commit()

            return redirect(url_for("admin.index"))

        flash(error)

    return render_template("admin/start.html")


@bp.route("/users", methods=("GET",))
@admin_required
def users():
    user_list = get_db().execute("SELECT * FROM user")

    return render_template("admin/users.html", user_list=user_list)


@bp.route("/send_emails", methods=("GET", "POST"))
@admin_required
def send_emails():
    if request.method == "POST":
        db = get_db()
        confirm = None
        error = None

        try:
            confirm = request.form["confirm"]
        except:
            error = "You must confirm to perform this action."

        user_list = db.execute("SELECT * FROM user WHERE match NOT NULL").fetchall()

        from os import environ

        try:
            password = environ["SECRET_SANTA_SMTP_PASS"]
        except KeyError:
            error = "Specify password on command line as SECRET_SANTA_SMTP_PASS"

        if error is None:
            if confirm is not None:
                import smtplib, ssl

                smtp_server = "mail.riseup.net"
                port = 587
                username = "codebam"
                sender = "merrychristmas@riseup.net"
                context = ssl.create_default_context()

                try:
                    server = smtplib.SMTP(smtp_server, port)
                    server.starttls(context=context)
                    server.login(username, password)

                    for user in user_list:
                        match = db.execute(
                            "SELECT * FROM user WHERE id = ?", (user["match"],)
                        ).fetchone()
                        message = """\
From: {}\r\nTo: {}\r\nSubject: Secret Santa Delivery\r\n\r\n
Here is your Secret Santa delivery! You are matched with {} {}! :)

Visit your Secret Santa account to see their wishlist and more.
""".format(
                            sender, user["email"], match["name"], match["surname"]
                        )
                        server.sendmail(sender, user["email"], message)
                except Exception as e:
                    print(e)
                finally:
                    server.quit()

            return redirect(url_for("admin.index"))

        flash(error)

    return render_template("admin/send_emails.html")
