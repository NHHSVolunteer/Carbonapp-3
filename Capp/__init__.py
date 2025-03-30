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

