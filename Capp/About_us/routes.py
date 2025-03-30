from flask import render_template, Blueprint
About_us=Blueprint('About_us', __name__)

@About_us.route('/About_us')
def About_us_home():
    return render_template('About_us.html', title='About_us')