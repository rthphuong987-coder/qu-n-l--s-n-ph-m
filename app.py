import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect,flash,url_for,session
import os
app = Flask(__name__)
app.secret_key="1234567"
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
          session["username"] = username
          return redirect("/dashboard")
        else:
            return "Sai email hoặc mật khẩu"

      return render_template("login.html")
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    keyword = request.args.get("keyword", "")
    category = request.args.get("category", "")

    c.execute("SELECT COUNT(DISTINCT category) FROM products")
    total_category = c.fetchone()[0]

    c.execute("SELECT SUM(price * quantity) FROM products")
    total_price = c.fetchone()[0] or 0

    c.execute("SELECT SUM(quantity) FROM products")
    total_quantity = c.fetchone()[0] or 0
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
        return redirect("/dashboard")

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if keyword:
       sql += " AND name LIKE ?"
       params.append(f"{keyword}")

    if category:
       sql += " AND category = ?"
       params.append(category)

    c.execute(sql, params)
    products = c.fetchall() 

    total_products = len(products)
    c.execute("SELECT DISTINCT category FROM products")
    categories = c.fetchall()
    conn.close()

    return render_template(
    'dashboard.html',
    products=products,
    categories=categories,
    keyword=keyword,
    total_products=total_products,
    total_category=total_category,
    total_price=total_price,
    total_quantity=total_quantity
)
@app.route("/products")
def products():
    keyword = request.args.get("keyword", "")

    return render_template(
        "products.html",
        keyword=keyword
    )

@app.route("/update_product", methods=["POST"])
def update_product():

    id = request.form["id"]
    name = request.form["name"]
    category = request.form["category"]
    price = request.form["price"]
    quantity = request.form["quantity"]
    code = request.form["code"]

    conn = sqlite3.connect("products.db")
    c = conn.cursor()

    c.execute(
        "SELECT image FROM products WHERE id=?",
        (id,)
    )

    old_image = c.fetchone()[0]

    image = request.files["image"]

    if image and image.filename != "":

        filename = secure_filename(image.filename)

        image.save(
            os.path.join("static/uploads", filename)
        )

    else:
        filename = old_image

    c.execute("""
        UPDATE products
        SET
            name=?,
            category=?,
            price=?,
            quantity=?,
            code=?,
            image=?
        WHERE id=?
    """,
    (
        name,
        category,
        price,
        quantity,
        code,
        filename,
        id
    ))

    conn.commit()
    conn.close()

    return redirect("/dashboard")

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