from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

auth_blueprint = Blueprint("auth", __name__)
con = get_db_connection()

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username= request.form.get("username")
        email = request.form.get("email")
        plain_password = request.form.get("password")
        password_hash = generate_password_hash(plain_password)

        print(username, email, password_hash)

        with con.cursor() as cur:
            cur.execute("""
            INSERT INTO users(username, email, password_hash) VALUES(%s, %s, %s)
                         """, (username,email, password_hash))
            
            con.commit()

        return redirect(url_for("notes.notes"))

    
    return render_template("register.html")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

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
    return render_template("login.html")