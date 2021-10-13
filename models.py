from app import db

class User(db.Document):
	email = db.EmailField(unique=True)
	senha = db.StringField(default=True)

    