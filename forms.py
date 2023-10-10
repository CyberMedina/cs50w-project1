from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField,  SubmitField
from wtforms.validators import DataRequired, Email, Length
from helpers import email_exists


class register_user(FlaskForm):
    name = StringField("Nombres", validators=[
        DataRequired(message="El campo debe ser rellenado"), 
        Length(max=10, min=3, message="El campo debe de tener entre 3 y 10 carácteres")
        ])
    lastname = StringField("Apellidos", validators=[
        DataRequired(), Length(max=10, min=3)
    ])
    email = EmailField("Correo eléctronico", validators=[
        DataRequired(),
        Email(message="El campo debe tener un correo eléctronico válido"),
        email_exists
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired()
    ])


    submit = SubmitField('Registrarse')