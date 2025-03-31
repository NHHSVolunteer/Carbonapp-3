from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3oueqkfdfas8ruewqndr8ewrewrouewrere44554'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_BINDS'] = {'transport': 'sqlite:///transport.db'}

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
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

    return app
