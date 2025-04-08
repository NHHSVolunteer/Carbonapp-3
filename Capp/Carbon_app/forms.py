from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField, BooleanField, StringField
from wtforms.validators import InputRequired, Optional, Length

class BaseTripForm(FlaskForm):
    kms = FloatField('Kilometers', validators=[InputRequired()])
    save_trip = BooleanField('Save this trip?')
    trip_name = StringField('Trip Name (if saving)', validators=[Optional(), Length(max=100)])

class BusForm(BaseTripForm):
    fuel_type = SelectField('Type of Fuel', validators=[InputRequired()], 
        choices=[('Diesel', 'Diesel'), ('CNG', 'CNG'), ('Petrol', 'Petrol'), ('No Fossil Fuel', 'No Fossil Fuel')])
    submit = SubmitField('Submit')

class CarForm(BaseTripForm):
    fuel_type = SelectField('Type of Fuel', validators=[InputRequired()],
        choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('No Fossil Fuel', 'No Fossil Fuel')])
    submit = SubmitField('Submit')

class PlaneForm(BaseTripForm):
    fuel_type = SelectField('Flight Type', validators=[InputRequired()],
        choices=[
            ('Short-haul flight (≤1,500 km)', 'Short-haul flight (≤1,500 km)'),
            ('Medium-haul flight (1,500–4,000 km)', 'Medium-haul flight (1,500–4,000 km)'),
            ('Long-haul flight (>4,000 km)', 'Long-haul flight (>4,000 km)')
        ])
    submit = SubmitField('Submit')

class FerryForm(BaseTripForm):
    fuel_type = SelectField('Passenger Type', validators=[InputRequired()],
        choices=[('Foot passenger', 'Foot passenger'), ('With car', 'With car')])
    submit = SubmitField('Submit')

class MotorbikeForm(BaseTripForm):
    fuel_type = SelectField('Type of Fuel', validators=[InputRequired()],
        choices=[('Petrol', 'Petrol'), ('Electric', 'Electric')])
    submit = SubmitField('Submit')

class BicycleForm(BaseTripForm):
    fuel_type = SelectField('Type', validators=[InputRequired()],
        choices=[('Standard', 'Standard')])
    submit = SubmitField('Submit')

class WalkForm(BaseTripForm):
    fuel_type = SelectField('Type', validators=[InputRequired()],
        choices=[('Standard', 'Standard')])
    submit = SubmitField('Submit')

from wtforms import SelectField
from wtforms.validators import DataRequired

class QuickLogForm(FlaskForm):
    trip_id = SelectField('Choose a saved trip', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Log this trip')
