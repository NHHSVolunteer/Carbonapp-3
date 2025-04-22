from flask import Flask, render_template, Blueprint
from Capp.models import Transport
from flask_login import current_user
from Capp import db 

home = Blueprint('home', __name__)

@home.route('/')
@home.route('/home')
def home_home():
    # Default to 0 emissions
    user_total_emissions = 0

    # Only calculate if user is logged in
    if current_user.is_authenticated:
        user_total_emissions = db.session.query(
            db.func.sum(Transport.co2)
        ).filter_by(author=current_user).scalar() or 0

        user_total_emissions = round(user_total_emissions, 2)

    # Pass the result to the template
    return render_template('home.html', user_total_emissions=user_total_emissions)
