import sqlite3
from flask import Flask, render_template, request, redirect

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

init_db()

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
@app.route('/dashboard')
def dashboard():

    products = []

    return render_template(
        'dashboard.html',
        products=products,
        total_products=len(products),
        total_orders=0
    )
@app.route("/products")
def products():
    keyword = request.args.get("keyword", "")

    return render_template(
        "products.html",
        keyword=keyword
    )
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
print(request.form)