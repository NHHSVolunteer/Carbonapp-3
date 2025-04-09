# Import necessary Flask modules and form
from flask import render_template, Blueprint
from Capp.users.forms import RegistrationForm  # Import the form used for user registration

# Create a Blueprint for the "register" section of your app.
# Blueprints help organize different parts of a Flask app into components.
register = Blueprint('register', __name__)

# Define the route (URL endpoint) for the registration page.
# This function will respond to both GET (loading the form) and POST (submitting the form) requests.
@register.route('/register', methods=['GET', 'POST'])
def register_home():
    # Create a new instance of the RegistrationForm to be used in the template.
    # Flask-WTF handles CSRF protection and field validation.
    form = RegistrationForm()

    # Render the template and send it the form object.
    # 'title' is passed to the template for display purposes.
    return render_template('Registration/register.html', title='register', form=form)
