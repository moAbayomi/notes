from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm
from database import get_db_connection

auth_blueprint = Blueprint("auth", __name__)
con = get_db_connection()

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username= form.username.data
        email = form.email_addy.data
        plain_password = form.password.data
        password_hash = generate_password_hash(plain_password)

        print(username, email, password_hash)

        try:
            with con.cursor() as cur:
                cur.execute("""
                INSERT INTO users(username, email, password_hash) VALUES(%s, %s, %s)
                            """, (username,email, password_hash))
                
                con.commit()
                return redirect(url_for("auth.login"))

        except Exception as e:
            con.rollback()
            print(f"database error:", 500)


    return render_template("register.html", form=form)

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email_addy.data
        password = form.password.data

        with con.cursor() as cur:
            cur.execute("""
            SELECT id, username, password_hash FROM users where email = %s

        """, (email,))
            
            data = cur.fetchone()

            if data and check_password_hash(data[2], password):
                print("user exists!")
                session["user_id"] = data[0]
                session["username"] = data[1]

                return redirect(url_for("notes.notes"))
            else:
                flash("invalid email or password", "danger")
    return render_template("login.html", form=form)


@auth_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("you have been logged out", "info")

    return redirect(url_for("auth.login"))