from flask import Flask, render_template,redirect,request,url_for,flash
from models import db,Product
import sqlite3
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()

    c.execute("SELECT * FROM products")
    products = c.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        products=products
    )
def products():

    keyword = request.args.get('keyword', '')

    products = Product.query.filter(
        Product.name.contains(keyword)
    ).all()

    return render_template(
        'products.html',
        products=products
    )
@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    conn = sqlite3.connect("products.db")
    c = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        code = request.form["code"]

        image = request.files["image"]

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join("static/uploads", filename))

            c.execute("""
                UPDATE products
                SET name=?, category=?, price=?, quantity=?, code=?, image=?
                WHERE id=?
            """, (name, category, price, quantity, code, filename, id))
        else:
            c.execute("""
                UPDATE products
                SET name=?, category=?, price=?, quantity=?, code=?
                WHERE id=?
            """, (name, category, price, quantity, code, id))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    c.execute("SELECT * FROM products WHERE id=?", (id,))
    product = c.fetchone()

    conn.close()

    return render_template("edit_product.html", product=product)