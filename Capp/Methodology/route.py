# Import functions needed to render pages and create a Blueprint
from flask import render_template, Blueprint

# Create a Blueprint named 'methodology'
# Blueprints allow you to group routes and functionality into separate files
methodology = Blueprint('methodology', __name__)

# Define a route for when users visit /methodology in the browser
@methodology.route('/methodology')
def methodology_home():
    # This function will be called when someone visits the /methodology URL
    # It returns the rendered 'methodology.html' page from your templates folder
    return render_template('methodology.html', title='methodology')
