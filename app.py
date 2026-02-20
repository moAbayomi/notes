import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, session
from database import get_db_connection
from routes.auth import auth_blueprint
from routes.notes import notes_blueprint
from helper import highlighter

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['WTF_CSRF_ENABLED'] = True
app.jinja_env.filters["highlight"] = highlighter


con = get_db_connection()
if con:
    print("heheh\ndatabase connected successfully!")

app.register_blueprint(auth_blueprint)
app.register_blueprint(notes_blueprint)

@app.route("/")
def index():
    user_id = session.get("user_id")
    if user_id:
        return redirect(url_for("notes.notes"))
    else:
        return redirect(url_for("auth.login"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")