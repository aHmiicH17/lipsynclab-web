# import sqlite3
# from flask import Flask, render_template, request, redirect, url_for, session, flash

# app = Flask(__name__)
# app.secret_key = 'your-secret-key'

# # Database connection
# def get_db_connection():
#     conn = sqlite3.connect('users.db')  # Replace with your database file
#     conn.row_factory = sqlite3.Row
#     return conn

# # Initialize the database
# def init_db():
#     conn = get_db_connection()
#     with open('database_setup.sql') as f:
#         conn.executescript(f.read())
#     conn.close()

# # Initialize the database when the app starts
# init_db()

# # Dashboard Route
# @app.route('/')
# def dashboard():
#     # if 'user_id' not in session:
#     #     return redirect(url_for('login'))
#     return render_template('dashboard.html')

# # Settings Route
# @app.route('/setting', methods=['GET', 'POST'])
# def setting():
#     # if 'user_id' not in session:
#     #     return redirect(url_for('login'))
#     return render_template('setting.html')

# # Signup Route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         first_name = request.form['firstName']
#         last_name = request.form['lastName']
#         email = request.form['email']
#         password = request.form['password']

#         conn = get_db_connection()
#         try:
#             conn.execute(
#                 'INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)',
#                 (first_name, last_name, email, password)
#             )
#             conn.commit()
#             flash("Signup successful! Please login.", "success")
#             return redirect(url_for('login'))
#         except sqlite3.IntegrityError:
#             flash("Email already exists. Please use a different email.", "error")
#         finally:
#             conn.close()
#     return render_template('signup.html')

# # Login Route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         conn = get_db_connection()
#         user = conn.execute(
#             'SELECT * FROM users WHERE email = ? AND password = ?',
#             (email, password)
#         ).fetchone()
#         conn.close()

#         if user:
#             session['user_id'] = user['id']
#             flash("Login successful!", "success")
#             return redirect(url_for('dashboard'))
#         else:
#             flash("Invalid credentials. Please try again.", "error")
#     return render_template('login.html')

# # Logout Route
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash("You have been logged out.", "info")
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError

# app = Flask(__name__)
# app.secret_key = 'your-secret-key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Define User model
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# # Dashboard Route
# @app.route('/')
# def dashboard():
#     return render_template('dashboard.html')

# # Settings Route
# @app.route('/setting', methods=['GET', 'POST'])
# def setting():
#     return render_template('setting.html')

# # Signup Route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         first_name = request.form.get('firstName')
#         last_name = request.form.get('lastName')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)

#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Signup successful! Please login.", "success")
#             return redirect(url_for('login'))
#         except IntegrityError as e:
#             db.session.rollback()
#             flash("Email already exists. Please use a different email.", "error")
#             print("IntegrityError:", e)  # Log the specific error for debugging
#         except Exception as e:
#             db.session.rollback()
#             flash("An error occurred. Please try again later.", "error")
#             print("Error:", e)  # Log any other exception for debugging
#     return render_template('signup.html')


# # Login Route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email, password=password).first()

#         if user:
#             session['user_id'] = user.id
#             flash("Login successful!", "success")
#             return redirect(url_for('dashboard'))
#         else:
#             flash("Invalid credentials. Please try again.", "error")
#     return render_template('login.html')

# # Logout Route
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash("You have been logged out.", "info")
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     # Manually create tables before running the app
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)



from flask import Flask,jsonify, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    settings = db.relationship('UserSettings', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# UserSettings model
class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    profile_pic = db.Column(db.String(120), default='default.jpg')
    country = db.Column(db.String(50), nullable=True)
    two_factor_enabled = db.Column(db.Boolean, default=False)

# Dashboard Route
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Settings Route
@app.route('/setting', methods=['GET', 'POST'])
def setting():
    if request.method == 'POST':
        # Logic to update user settings can go here
        pass
    return render_template('setting.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']

        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! Please login.", "success")
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return {"message": "Email already exists. Please use a different email."}, 400
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"message": "An error occurred. Please try again later."}, 500
    return render_template('signup.html')

    #     try:
    #         db.session.add(new_user)
    #         db.session.commit()
    #         flash("Signup successful! Please login.", "success")
    #         return redirect(url_for('login'))
    #     except IntegrityError:
    #         db.session.rollback()
    #         flash("Email already exists. Please use a different email.", "error")
    # return render_template('signup.html')

#Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "error")
    return render_template('login.html')





# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
