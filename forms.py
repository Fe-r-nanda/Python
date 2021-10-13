import models
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from flask.ext.mongoengine.wtf.orm import validators

user_form = model_form(models.User, exclude=['senha'])

class SignupForm(user_form):
    password = PasswordField('Senha', validators=[validators.Required(), validators.EqualTo('confirmar', message='As senhas devem ser compatíveis')])
    confirm = PasswordField('Confirme a senha')


class LoginForm(user_form):
    password = PasswordField('Senha',validators=[validators.Required()])
