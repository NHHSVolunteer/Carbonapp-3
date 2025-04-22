import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Handles database operations (ORM)
from flask_bcrypt import Bcrypt          # For hashing passwords securely
from flask_login import LoginManager     # For managing user sessions and login states

# Create extension instances outside the app factory so we can use them globally
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Tell Flask-Login where to redirect users who aren’t logged in
login_manager.login_view = 'users.login'  # Refers to the login route in 'users' blueprint
login_manager.login_message_category = 'info'  # Flash message category 

def create_app():
    # Create the actual Flask app object
    app = Flask(__name__)

    # Load environment variables safely using os.environ.get()
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_fallback')  # Keep sessions secure
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Main database (PostgreSQL on AWS)

    # Some configuration
    app.config['SQLALCHEMY_BINDS'] = {
        'transport': app.config['SQLALCHEMY_DATABASE_URI'] 
    }

    # Initialize all extensions with the Flask app instance
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register all the blueprints (modular parts of the app)
    from Capp.home.routes import home
    from Capp.Methodology.route import methodology
    from Capp.Carbon_app.routes import carbon_app
    from Capp.users.routes import users
    from Capp.About_us.routes import About_us

    app.register_blueprint(home)
    app.register_blueprint(methodology)
    app.register_blueprint(carbon_app)
    app.register_blueprint(users)
    app.register_blueprint(About_us)

    return app  # Return the configured app
