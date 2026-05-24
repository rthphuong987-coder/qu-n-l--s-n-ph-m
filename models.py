from app import db

class User(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True)
    password =db.Column(db.String(100),unique=True)
class Product(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    price =db.Column(db.Integer)