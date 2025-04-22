# Importing necessary modules from Flask
# - render_template is used to render HTML templates
# - Blueprint allows us to organize our Flask app into smaller, reusable components
from flask import render_template, Blueprint

# Creating a blueprint called 'About_us'.
# Blueprints are used to group related routes (URLs) together in Flask.
# It helps you break your application into modules and keep things organized.
About_us = Blueprint('About_us', __name__)

# Defining a route for the URL path "/About_us"
# When a user visits this path, the function below is triggered.
@About_us.route('/About_us')
def About_us_home():
    # This function returns an HTML page called "About_us.html"
    # It also passes a variable called 'title' to the HTML, which you can use in your template.
    return render_template('about_us.html', title='About_us')
