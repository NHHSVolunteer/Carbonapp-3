# Import Flask tools
from flask import Flask, render_template, Blueprint

# Create a new Blueprint for the homepage
# A Blueprint allows us to split up the app into reusable components
home = Blueprint('home', __name__)

# Define two URL routes:
# '/' is the root URL (e.g., https://example.com)
# '/home' is an alternative URL that also points to the homepage
@home.route('/')
@home.route('/home')
def home_home():
    # Render the "home.html" template
    # This file should be located in the templates folder (e.g., templates/home.html)
    return render_template('home.html')
