from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
@app.route("/dashboard")
def dashboard():
     products = []

     return render_template(
        "dashboard.html",
        products=0,
        total_products=len(products),
        total_orders=0
    )
@app.route('/products')
def products():

    keyword = request.args.get('keyword', '')

    products = Product.query.filter(
        Product.name.contains(keyword)
    ).all()

    return render_template(
        'products.html',
        products=products
    )