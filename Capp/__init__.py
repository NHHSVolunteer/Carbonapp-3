from flask import Flask

application = Flask(__name__)

from Capp.home.routes import home
from Capp.Methodology.route import methodology
from Capp.Carbon_app.routes import Carbon_app
from Capp.register.routes import register
from Capp.About_us.routes import About_us

application.register_blueprint(home)
application.register_blueprint(methodology)
application.register_blueprint(Carbon_app)
application.register_blueprint(register)
application.register_blueprint(About_us)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

application = Flask(__name__)

# application.config['SECRET_KEY'] = os.environ['SECRET_KEY']  
application.config['SECRET_KEY'] = '3oueqkfdfas8ruewqndr8ewrewrouewrere44554'

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
application.config['SQLALCHEMY_BINDS'] ={'transport': 'sqlite:///transport.db'}


db = SQLAlchemy(application)
bcrypt = Bcrypt(application)
login_manager= LoginManager(application)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


