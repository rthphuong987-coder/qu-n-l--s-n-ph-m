from app import db

class User(db.Model):

    id=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True)
    password =db.Column(db.String(100),unique=True)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    price = db.Column(db.Interger)

    image = db.Column(db.String(300))

    category = db.Column(db.String(100))
    
    quantity = db.Column(db.Interger)