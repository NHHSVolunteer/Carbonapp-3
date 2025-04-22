# Import necessary Flask extensions
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # For database management
from flask_bcrypt import Bcrypt          # For hashing passwords securely
from flask_login import LoginManager     # For managing user sessions

# Create instances of the extensions
db = SQLAlchemy()          # Used for all database operations
bcrypt = Bcrypt()          # Used to hash and check passwords
login_manager = LoginManager()  # Handles login sessions

# Set the default route where users are redirected if login is required
login_manager.login_view = 'users.login'  # Flask will redirect to this view if @login_required fails
login_manager.login_message_category = 'info'  # Flash message category (used in Bootstrap alert class)

# This function creates the full Flask application instance
def create_app():
    app = Flask(__name__)  # Create the Flask app object

    DBVAR = 'postgresql://postgres:Passord1@awseb-e-rnp7np9gr8-stack-awsebrdsdatabase-ploqwsbxmo0u.cj4ccg8qk3wp.eu-north-1.rds.amazonaws.com:5432/ebdb'
    app.config['SQLALCHEMY_DATABASE_URI'] = DBVAR
    app.config['SQLALCHEMY_BINDS']={'transport':DBVAR}


    # Basic app configuration
    app.config['SECRET_KEY'] = '3oueqkfdfas8ruewqndr8ewrewrouewrere44554'  # Used to keep sessions secure
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Main database for user accounts

    # Additional database (bound to the 'transport' key) for transport-related data
    #app.config['SQLALCHEMY_BINDS'] = {
     #   'transport': 'sqlite:///transport.db'
    

    # Initialize the extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import and register all the different blueprints (modular app structure)
    from Capp.home.routes import home                     # Homepage routes
    from Capp.Methodology.route import methodology        # Methodology info page
    from Capp.Carbon_app.routes import carbon_app         # Core app functionality (logging emissions)
    from Capp.users.routes import users                   # Registration and login system
    from Capp.About_us.routes import About_us             # Team information

    # Register blueprints with the Flask app
    app.register_blueprint(home)
    app.register_blueprint(methodology)
    app.register_blueprint(carbon_app)
    app.register_blueprint(About_us)
    app.register_blueprint(users)

    

    return app  # Return the configured app instance
