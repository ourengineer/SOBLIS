# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from_pymongo PyMongo
from_bcrypt Bcrypt
from functools wraps
 os

app =(__name__)
app.config['MONGO_URI = "mongodb://localhost:27017/body_language_db"
app.secret_key = os.urandom(24)
mongo = PyMongo(app)
 = Bcrypt(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in:
            return(url_for('login'))
 f(*args, **)
   

@app.route('/')
@login
def dashboard():
   ('.html')

@app('/login', methods=['GET', 'POST'])
def():
    if.method == 'POST':
 email =.form['email password =.form[' user = mongo.db.users.find_one({'email':})
 if user and bcrypt.check_password_hash(user[''],):
['user_id = str(user['_id'])
(url_for(''))
   ('login.html')

@app('/register',=['GET', 'POST'])
def register():
    if == 'POST':
 =.form['email =.generate_hash(request.form['']).decode('utf-8')
.db.insert_one({'email':, '':})
(url_for('login'))
   ('.html')

@app('/api/upload_inertia',=['POST'])

def upload_inertia():
    body_data =.json
   .db.inertia_records_one(body_data)
   ({"message": "Inertia data recorded."}), 201

if __name__ == '__main__':
    app.run(debug=True)