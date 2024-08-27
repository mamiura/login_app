from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', user=current_user)

@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username  # Store username in session
            return redirect(url_for('profile'))
        else:
            return 'Login failed! Please check your credentials and try again.'

    return render_template('login.html', user=current_user)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return 'There was an issue adding the user. Please try again.'

    return render_template('signup.html', user=current_user)

# Route for Logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Correct session handling
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
