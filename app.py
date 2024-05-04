from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

# The secret key for session security and CSRF protection
app.config['SECRET_KEY'] = 'TeamRed'
# Configuration for the database, use SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserInfo.db'
# Instance for database interactions
db = SQLAlchemy(app)

# Flask-Login manager for handling user sessions and authentication
login_manager = LoginManager(app)
# Default route for login page
login_manager.login_view = 'login'


# Define the User model
class User(db.Model, UserMixin):
    __tablename__ = 'user' # Table name
    id = db.Column(db.Integer, primary_key=True) # Primary key is ID
    username = db.Column(db.String(80), unique=True, nullable=False) # Username must be unique
    password_hash = db.Column(db.String(128), nullable=False) # Store hashed password, for security purpose
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # Email must be unique

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# User loader function required by Flask-Login to manage the user session
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Fetch the user by ID

"""
// For creating database and testing only
def create_test_user():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='test@email.com').first():
            hashed_password = generate_password_hash('testpassword')
            new_user = User(
                username='testuser',
                password_hash=hashed_password,
                first_name='Test',
                last_name='User',
                email='test@email.com'
            )
            db.session.add(new_user)
            db.session.commit()
            print('Test user created.')
        else:
            print('Test user already exists.')
"""

# Form for user registration
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    # Require password and confirm_password are the same
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Route for handling registration requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Redirect authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    # Process form submission
    if form.validate_on_submit():
        # Check if the email is already in use
        existing_user = User.query.filter_by(email=form.email.data).first()

        # Inform the user about the email issue
        if existing_user:
            flash('Email already in use. Please use a different email.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data,
            password_hash=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )

        try:
            db.session.add(new_user) # Add the new user to the database
            db.session.commit() # Commit the session to save the user
            flash('Your account has been created! You are now able to log in.', 'success')
            # For checking purpose
            # print('New user created:', new_user)
            return redirect(url_for('login')) # Redirect the user to the login page
        except IntegrityError:
            db.session.rollback() # Rollback the transaction on error
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('register'))  # Redirect on error
    else: # Form validation failure
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                print(f"Error in {fieldName}: {err}")

    # Re-render the form if validation failure
    return render_template('register.html', title='Register', form=form)


# Route for handling login requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect authenticated users
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # Process form submission
    if form.validate_on_submit():
        # Queries the database for a user with the submitted username
        user = User.query.filter_by(username=form.username.data).first()

        # Checks if the user exists and the password is correct
        if user and check_password_hash(user.password_hash, form.password.data):
            # Logs the user in and redirects to the home page
            login_user(user)
            return redirect(url_for('index'))  # Or another page
        else:
            # Shows an error message if login is unsuccessful
            flash('Login Unsuccessful. Please check username and password', 'danger')

    # Re-render the form if validation failure
    return render_template('login.html', title='Login', form=form)


# Route for handling login requests
@app.route('/logout')
def logout():
    logout_user() # Logs out the current user
    return redirect(url_for('login')) # Redirect to the login page


# Route for handling game, logged in requires
@app.route('/')
@login_required
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

