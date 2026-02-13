from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_db_connection
from helper import format_note_date

notes_blueprint = Blueprint("notes", __name__)


@notes_blueprint.route("/", methods=["GET"])
def notes():
    user_id = session.get("user_id")
    username = session.get("username")
    if user_id:
        con = get_db_connection()
        try:
            with con.cursor() as cur:
                cur.execute("""
                DELETE FROM notes 
                WHERE user_id=%s 
                AND (title = '' OR title IS NULL) 
                AND (content = '' OR content IS NULL)
                """, (user_id,))
                con.commit()
                cur.execute("""
                SELECT id, title, content, created_at from notes
                ORDER BY created_at DESC
                """)
                notes = cur.fetchall()
        except Exception as e:
            con.rollback()
        finally:
            con.close()
        
        return render_template("notes.html", username=username, notes=notes, format_note_date=format_note_date)
    else:
        return redirect(url_for("auth.login"))   



@notes_blueprint.route("/get-note/<id>")
def get_note(id):
    user_id = session.get("user_id")
    if user_id:
        con = get_db_connection()
        try:

            with con.cursor() as cur:
                cur.execute("""
                DELETE FROM notes 
                WHERE user_id=%s 
                AND (title = '' OR title IS NULL) 
                AND (content = '' OR content IS NULL)
                AND id != %s
                RETURNING id
            """, (user_id, id))
                deleted_notes = cur.fetchall()
                con.commit()
                cur.execute("""
                    SELECT id, title, content, created_at FROM notes where user_id=%s AND id=%s
                    """, (user_id, id))
                note = cur.fetchone()
        except Exception as e:
            con.rollback()
        finally:
            con.close()

        if not note:
            return "Note not found", 404
        
        edited_temp = render_template("content_editable.html", note=note,format_note_date=format_note_date)
        
        for row in deleted_notes:
            deleted_id = row[0]
            edited_temp += f'<div id="notes-{deleted_id}" hx-swap-oob="delete"></div>'

        return edited_temp


@notes_blueprint.route("/delete/<int:note_id>", methods=["DELETE"])
def delete(note_id):
   user_id = session.get("user_id")
   if user_id:
        con = get_db_connection()
        try:

            with con.cursor() as cur:
                cur.execute("""
                    DELETE FROM notes where user_id=%s AND id=%s
                    """, (user_id, note_id))
                con.commit()
        finally:
            con.close()

        return ""
           
@notes_blueprint.route("/edit/<int:note_id>", methods=["PUT"])
def edit(note_id):
    user_id = session.get("user_id")
    if user_id:
        con = get_db_connection()
        content = request.form.get("content", "").strip()
        
        lines = content.split("\n", 1)

        title = lines[0][:50] if lines[0] else "" 
        content = lines[1] if len(lines) > 1 else "" 
           
        try:
            with con.cursor() as cur:
                cur.execute("""
                UPDATE notes SET title=%s, content=%s WHERE 
                user_id=%s AND id=%s
                """, (title, content, user_id, note_id))
            
                con.commit()
                cur.execute("SELECT id, title, content, created_at FROM notes WHERE id=%s", (note_id,))
                updated = cur.fetchone()

                """ if not title and not content:
                # We return a special OOB trigger that deletes the sidebar element
                # but returns NOTHING for the editor (so the editor stays as is)
                    return f'<div id="notes-{note_id}" hx-swap-oob="delete"></div>' """
        except Exception as e:
            con.rollback()
        finally:
            con.close()

        return render_template("singlenote.html", note=updated, is_edit=True, format_note_date=format_note_date)
    
    else:
        return "unauthorized", 401


@notes_blueprint.route("/new", methods=["GET", "PUT"])
def new_note():
    user_id = session.get("user_id")
    if user_id:
        title = ""
        content = ""

        con = get_db_connection()

        try:
            with con.cursor() as cur:
                cur.execute("""
                 INSERT INTO notes (user_id, title, content) 
                        VALUES(%s, %s, %s)
                        RETURNING id, title, content, created_at 
                """, (user_id, title, content))
                con.commit()

                note = cur.fetchone()
        except Exception as e:
            con.rollback()
        finally:
            con.close()

        return render_template("create_response.html", note=note, is_new=True,  format_note_date=format_note_date)

    else:
        return redirect(url_for("auth.login"))           
