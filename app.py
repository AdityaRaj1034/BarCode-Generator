from flask import Flask, render_template, redirect, jsonify, request, url_for
import sqlite3
from barcode import EAN13 
from barcode.writer import ImageWriter 
import random

app = Flask(__name__)

def generate_unique_number():
    while True:
        number = random.randint(1000000000000, 9999999999999)
        if is_unique(number):
            return number

def is_unique(number):
    conn = sqlite3.connect('database.db')
    select_user = "SELECT COUNT(*) FROM products WHERE p_id = ?"
    cursor = conn.execute(select_user, (number,))
    result = cursor.fetchone()
    if result[0]==0:
        return True


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/Signup.html")
def signin():
    return render_template("Signup.html")


@app.route("/index.html")
def home2():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/login.html")
def login():
    return render_template("login.html")
  

@app.route('/signup.html', methods=['POST'])
def signup1():
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        username = request.form['email']
        select_user = "SELECT COUNT(*) FROM users WHERE email = ?"
        cursor = conn.execute(select_user, (username,))
        result = cursor.fetchone()
        if result[0] > 0:
            return render_template('signup.html',use="Email is already exits")
        name = request.form['name']
        passw= request.form['pass']
        conpass= request.form['conpass']
        phone= request.form['phone']
        if conpass==passw:
            insert_user = "INSERT INTO users (name, email,phone, password) VALUES (?, ?, ?, ?)"
            conn.execute(insert_user, (name,username,phone, passw))
            conn.commit()
            return render_template('message.html',mes="login.html")
        else:
            return render_template('signup.html',err="Passsword does not matched")



@app.route('/login.html', methods=['POST'])
def signin_():
    if request.method == 'POST':
        username = request.form['username']
        passw= request.form['pass']
        conn = sqlite3.connect('database.db')
        select_user = "SELECT COUNT(*) FROM users WHERE email = ?"
        cursor = conn.execute(select_user, (username,))
        result = cursor.fetchone()
        if result[0] == 0:
            return render_template('login.html',use="Email is not exits")
        select_query = "SELECT password FROM users WHERE email= ?"
        cursor = conn.execute(select_query, (username,))
        result = cursor.fetchone()
        select_query = f"SELECT user_id FROM users  WHERE email = ?"
        cursor = conn.execute(select_query, (username,))
        name = cursor.fetchone()
        if result is not None and result[0] == passw:
            select_query = f"SELECT * FROM products WHERE user_id = ?"
            cursor = conn.execute(select_query, (name[0],))
            data = cursor.fetchall()
            conn.close()
            return render_template("data.html",user_id=name[0],data=data)
        else:    
            return render_template("login.html", err="Password invalid")

@app.route('/add_product', methods=['POST'])
def pr():
    if request.method == 'POST':
        user_id=request.form['user_id']
        return render_template('product.html',user_id=user_id)

@app.route('/back2', methods=['POST'])
def pr3():
    if request.method == 'POST':
        user_id=request.form['user_id']
        print(user_id)
        print(type(user_id))
        conn = sqlite3.connect('database.db')
        select_query = f"SELECT * FROM products WHERE user_id = ?"
        cursor = conn.execute(select_query, (user_id,))
        data = cursor.fetchall()
        conn.close()
        return render_template('data.html',user_id=user_id,data=data)


@app.route('/product.html', methods=['POST'])
def pr1():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        description = request.form.get('des')
        product_id = generate_unique_number()
        print("Unique 10-digit number:", product_id)
        my_code = EAN13(str(product_id), writer=ImageWriter()) 
        my_code.save(f"static/barcode/{product_id}")
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, description, price, quantity,p_id,user_id) VALUES (?, ?, ?, ?,?,?)',
                       (name, description, price, quantity,product_id,user_id))
        conn.commit()
        conn.close()
        return render_template('message2.html',user_id=user_id)

    

if __name__ == '__main__':
    app.run(debug=True)