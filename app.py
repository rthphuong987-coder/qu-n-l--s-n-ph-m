from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = []

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users.append({
            'username': username,
            'password': password
        })

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and user['password'] == password:
                return "Đăng nhập thành công"

        return "Sai tài khoản hoặc mật khẩu"

    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)