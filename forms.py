from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required



class LoginForm(FlaskForm):
    usuario = StringField('Nombre de usuario', validators=[Required()])
    password = PasswordField('Contraseña', validators=[Required()])
    enviar = SubmitField('Ingresar')



class SaludarForm(FlaskForm):
    usuario = StringField('Buscar: ', validators=[Required()])
    enviar = SubmitField('Buscar:')


class RegistrarForm(LoginForm):
    password_check = PasswordField('Verificar Contraseña', validators=[Required()])
    enviar = SubmitField('Registrarse')


class ConsultaPaisForm(FlaskForm):
    pais = StringField('Búsqueda: ')
    submit = SubmitField('Buscar')
