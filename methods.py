import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from app import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

import forms
from libs.User import User

auth_flask_login = Blueprint('auth_flask_login', __name__)

@auth_flask_login.route("/signin", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)
     	if user and flask_bcrypt.check_password_hash(user.senha,request.form["senha"]) and user.is_active(): remember = request.form.get("remember", "no") == "yes"

	if login_user(user, remember=remember):
		       flash("Logado!")
	else:
		       flash("Login inválido")

    return render_template("/auth/login.html")

#
# Route desabilitada - permite a route liberar o cadastro de usuário
#
@auth_flask_login.route("/signup", methods=["GET","POST"])
def register():
	
	registerForm = forms.SignupForm(request.form)
	current_app.logger.info(request.form)

	if request.method == 'POST' and registerForm.validate() == False:
		current_app.logger.info(registerForm.errors)
		return "Não foi possível concluir o cadastro"

	elif request.method == 'POST' and registerForm.validate():
		email = request.form['email']
		
		
		password_hash = flask_bcrypt.generate_password_hash(request.form['senha'])

		user = User(email,password_hash)
		print (user)

		try:
			user.save()
			if login_user(user, remember="no"):
				flash("Logado!")
				return redirect('/')
			else:
				flash("Login inválido")

		except:
			flash("E-mail inválido")
			current_app.logger.error("Erro ao cadastrar - e-mail duplicado")

	templateData = {

		'form' : registerForm
	}

	return render_template("/auth/register.html", **templateData)

@auth_flask_login.route("/reauth", methods=["GET", "POST"])
@login_required
def reauth():
    if request.method == "POST":
        confirm_login()
        flash(u"Reauthenticated.")
        return redirect(request.args.get("next") or '/admin')
    
    templateData = {}
    return render_template("/auth/reauth.html", **templateData)


@auth_flask_login.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Deslogado.")
    return redirect('/signin')

@login_manager.unauthorized_handler
def unauthorized_callback():
	return redirect('/signin')

@login_manager.user_loader
def load_user(id):
	if id is None:
		redirect('/signin')
	user = User()
	user.get_by_id(id)
	if user.is_active():
		return user
	else:
		return None