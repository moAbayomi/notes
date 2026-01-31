from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

notes_blueprint = Blueprint("notes", __name__)
con = get_db_connection()


@notes_blueprint.route("/", methods=["GET", "POST"])
def notes():
    
    user_id = session.get("user_id")
    if user_id:
        username = session["username"]
    

        if request.method == "POST":

            if request.is_json:
                data = request.get_json()
                action = data.get("action")
                target_note = data.get("id")
                new_content = data.get("content")
            else:
                action = request.form.get("action")
                target_note = request.form.get("note_id")
                new_content = request.form.get("content")

            if action == "delete":
                with con.cursor() as cur:
                    cur.execute("""
                    DELETE FROM notes where id=%s AND user_id=%s
                    """,(target_note, user_id))

                    con.commit()

            elif action == "edit":
                
                   
                try:

                    with con.cursor() as cur:
                        cur.execute("""
                        UPDATE notes
                        set content=%s 
                        WHERE id=%s AND user_id=%s
                        """, (new_content, target_note, user_id))

                        con.commit()
                    return {"status": "success"}
                except Exception as e:
                    con.rollback() 
                    print(f"SQL Error: {e}")
                    return {"status": "error"}, 500

            
            else:
                title = request.form.get("title")
                content = request.form.get("content")

                
                with con.cursor() as cur:
                    cur.execute("""
                    INSERT INTO notes (user_id, title, content) 
                    VALUES(%s, %s, %s)
                    """, (user_id, title, content))
                    con.commit()

        with con.cursor() as cur:
            cur.execute("""
            SELECT id, title, content, created_at 
            FROM notes WHERE user_id = %s ORDER BY created_at DESC
            """, (user_id,))
            notes = cur.fetchall()
        return render_template("notes.html", username=username, notes=notes)
    else:
        return redirect(url_for("auth.login"))