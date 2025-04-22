# Import necessary Flask extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # For handling database operations
from flask_bcrypt import Bcrypt          # For securely hashing passwords
from flask_login import LoginManager     # For user session management
import os                                # For accessing environment variables

# Create instances of the extensions
db = SQLAlchemy()                        # Database object
bcrypt = Bcrypt()                        # Password hashing object
login_manager = LoginManager()           # User session manager

# Set the default login view and flash category for login-required redirects
login_manager.login_view = 'users.login'        # If user is not logged in, redirect here
login_manager.login_message_category = 'info'   # Flash message style (Bootstrap class)

# Function to create the Flask app
def create_app():
    app = Flask(__name__)  # Create the Flask app

    # Database connection string (for AWS RDS)
    DBVAR = 'postgresql://postgres:Passord1@awseb-e-rnp7np9gr8-stack-awsebrdsdatabase-ploqwsbxmo0u.cj4ccg8qk3wp.eu-north-1.rds.amazonaws.com:5432/ebdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = DBVAR

    # If you're using more than one database, you can bind additional ones like this:
    app.config['SQLALCHEMY_BINDS'] = {'transport': DBVAR}

    # Use environment variable for secret key (set this in your deployment environment!)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')

    # Initialize Flask extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register Blueprints (modular parts of your app)
    from Capp.home.routes import home
    from Capp.Methodology.route import methodology
    from Capp.Carbon_app.routes import carbon_app
    from Capp.users.routes import users
    from Capp.About_us.routes import About_us

    app.register_blueprint(home)
    app.register_blueprint(methodology)
    app.register_blueprint(carbon_app)
    app.register_blueprint(About_us)
    app.register_blueprint(users)

    return app  # Return the fully configured Flask app
