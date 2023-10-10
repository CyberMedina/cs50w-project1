import os

from functools import wraps
from flask import session, redirect, jsonify, request, url_for
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from sqlalchemy.orm import scoped_session, sessionmaker

from wtforms.validators import ValidationError # Acá utlizaremos esto para capturar los errores en los formularios

# Set up database
engine= create_engine(os.getenv("DATABASE_URL"), pool_size=20, max_overflow=30)
db = scoped_session(sessionmaker(bind=engine))


# Deccorador para validar si un usuario está loguado o no
def login_requiredUser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index',  registerSuccess=0))
        return f(*args, **kwargs)
    return decorated_function


#Función para validar si un correo eléctronico existe en la base de datos
def email_exists(form, field):
        query2 = text("SELECT * FROM users WHERE (email = :email) LIMIT 1")
        userExist = db.execute(query2, {"email":field.data}).fetchone()

        if userExist:
            print("SI ENTRÓ")
            raise ValidationError("El correo electrónico ya está registrado.")
