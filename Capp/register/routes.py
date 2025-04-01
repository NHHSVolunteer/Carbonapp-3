from flask import render_template, Blueprint
from Capp.users.forms import RegistrationForm  # or wherever your form is
register = Blueprint('register', __name__)

@register.route('/register', methods=['GET', 'POST'])
def register_home():
    form = RegistrationForm()  # ← create the form object
    return render_template('Registration/register.html', title='register', form=form)
