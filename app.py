import os

from flask import Flask, render_template, request, redirect 
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

# Criando app Flask
app = Flask("FlaskLoginApp")

# Interligando com banco de dados
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'FlaskLogin'}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.debug = os.environ.get('DEBUG',False)

db = MongoEngine(app) # conectar MongoEngine com Flask App
app.session_interface = MongoEngineSessionInterface(db) 

# Flask BCrypt usado para as senhas
flask_bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
