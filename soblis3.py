# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from functools import wraps
import os

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/body_language_db"
app.secret_key = os.urandom(24)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        mongo.db.users.insert_one({'email': email, 'password': password})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/api/upload_inertia', methods=['POST'])
@login_required
def upload_inertia():
    body_data = request.json
    mongo.db.inertia_records.insert_one(body_data)
    return jsonify({"message": "Inertia data recorded."}), 201

if __name__ == '__main__':
    app.run(debug=True)