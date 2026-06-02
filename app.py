import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect,flash,url_for
import os
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def init_product_db():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        quantity INTEGER,
        code TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()
init_product_db()

users = []
@app.route('/')
def home():
     return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
     if request.method == 'POST':
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            return "Mật khẩu không khớp"

        with sqlite3.connect("users.db") as conn:
           c = conn.cursor()

           c.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )

        conn.commit()

        return redirect("/login")

     return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
        email = request.form.get('email')
        username = request.form['username']
        password = request.form.get('password')
        with sqlite3.connect("users.db") as conn:
         c = conn.cursor()

         c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        if user:
            return redirect("/dashboard")
        else:
            return "Sai email hoặc mật khẩu"

      return render_template("login.html")
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    conn = sqlite3.connect("products.db")
    c = conn.cursor()

    if request.method == 'POST':

        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        quantity = request.form['quantity']
        code = request.form['code']

        image = request.files['image']

        filename = ""

        if image and image.filename != "":
            filename = secure_filename(image.filename)

            os.makedirs("static/uploads", exist_ok=True)

            image.save(
                os.path.join("static/uploads", filename)
            )

        c.execute("""
            INSERT INTO products
            (name, category, price, quantity, code, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            category,
            price,
            quantity,
            code,
            filename
        ))

        conn.commit()

    c.execute("SELECT * FROM products")
    products = c.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        products=products,
        total_products=len(products),
        total_category=0,
        total_price=0
    )
@app.route("/products")
def products():
    keyword = request.args.get("keyword", "")

    return render_template(
        "products.html",
        keyword=keyword
    )



@app.route("/edit_product/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    product = product.query.get_or_404(id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.category = request.form["category"]
        product.price = float(request.form["price"])
        product.quantity = int(request.form["quantity"])
        product.code = request.form["code"]

        image = request.files["image"]

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            product.image = filename

        db.session.commit()

        flash("Cập nhật sản phẩm thành công!")
        return redirect(url_for("dashboard"))

    return render_template(
        "edit_product.html",
        product=product
    )

@app.route("/delete_product/<int:id>")
def delete_product(id):

    conn = sqlite3.connect("products.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM products WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
print(request.form)