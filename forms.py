from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, Length 
from database import get_db_connection


class RegisterForm(FlaskForm):
    # you should check if username is available also. i should absolutely include that!
    username = StringField("what would be your preferred username", validators=[DataRequired(), Length(min=4, max=20)])
    email_addy = StringField("input email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("create")

    def validate_username(self, username):
        con = get_db_connection()
        try:
            with con.cursor() as cur:
                cur.execute("""
                SELECT id FROM users WHERE username=%s
                """, (username.data,))

                data = cur.fetchone()
                if data:
                    raise ValidationError("that username already exists!")
        except ValidationError:
            raise

        except Exception as e:
            print("db error during validation:", e)
        finally:
             con.close()



    def validate_email_addy(self, email_addy):
        con = get_db_connection()
        try:
            with con.cursor() as cur:
                cur.execute("""
                SELECT id FROM users where email=%s
                """, (email_addy.data,))
                data = cur.fetchone()

                if data:
                    raise ValidationError("another user exists with this email. stop right there!")
        except ValidationError:
            raise
        except Exception as e:
            print("error with db connection: ", e)
        finally:
            con.close()




class LoginForm(FlaskForm):
    email_addy = StringField("your email", validators=[DataRequired()])
    password = PasswordField("your password", validators=[DataRequired()])
    submit = SubmitField("login")


class NoteForm(FlaskForm):
    title = StringField("note title")
    note = TextAreaField("enter your note")
    submit = SubmitField("save")