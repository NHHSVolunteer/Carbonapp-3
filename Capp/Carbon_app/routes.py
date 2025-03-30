from flask import render_template, Blueprint
Carbon_app=Blueprint('Carbon_app', __name__)

@Carbon_app.route('/carbon_app')
def carbon_app():
    return render_template('carbon_app.html', title='carbon_app')
