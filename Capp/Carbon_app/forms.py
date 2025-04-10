# Import base class for forms in Flask
from flask_wtf import FlaskForm

# Import commonly used field types and validators
from wtforms import SubmitField, SelectField, FloatField, BooleanField, StringField
from wtforms.validators import InputRequired, Optional, Length

# -------------------------------
# Base class for shared form logic
# -------------------------------
class BaseTripForm(FlaskForm):
    # Field for entering distance (in kilometers)
    kms = FloatField('Kilometers', validators=[InputRequired()])

    # Checkbox to let users choose whether to save the trip
    save_trip = BooleanField('Save this trip?')

    # Text input for giving a name to the trip (if saving it)
    trip_name = StringField('Trip Name (if saving)', validators=[Optional(), Length(max=100)])


# -------------------------------
# Form for Bus trips
# -------------------------------
class BusForm(BaseTripForm):
    # Dropdown for fuel type used by the bus
    fuel_type = SelectField('Type of Fuel', validators=[InputRequired()], 
        choices=[('Diesel', 'Diesel'), ('CNG', 'CNG'), ('Petrol', 'Petrol'), ('No Fossil Fuel', 'No Fossil Fuel')])
    submit = SubmitField('Submit')


# -------------------------------
# Form for Car trips
# -------------------------------
class CarForm(BaseTripForm):
    fuel_type = SelectField('Type of Fuel', validators=[InputRequired()],
        choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('No Fossil Fuel', 'No Fossil Fuel')])
    submit = SubmitField('Submit')


# -------------------------------
# Form for Plane trips
# -------------------------------
class PlaneForm(BaseTripForm):
    # Instead of fuel type, we use flight range categories
    fuel_type = SelectField('Flight Type', validators=[InputRequired()],
        choices=[
            ('Short-haul flight (≤1,500 km)', 'Short-haul flight (≤1,500 km)'),
            ('Medium-haul flight (1,500–4,000 km)', 'Medium-haul flight (1,500–4,000 km)'),
            ('Long-haul flight (>4,000 km)', 'Long-haul flight (>4,000 km)')
        ])
    submit = SubmitField('Submit')


# -------------------------------
# Form for Ferry trips
# -------------------------------
class FerryForm(BaseTripForm):
    # User specifies whether they’re walking on board or bringing a car
    fuel_type = SelectField('Passenger Type', validators=[InputRequired()],
        choices=[('Foot passenger', 'Foot passenger'), ('With car', 'With car')])
    submit = SubmitField('Submit')


# -------------------------------
# Form for Motorbike trips
# -------------------------------
class MotorbikeForm(BaseTripForm):
    fuel_type = SelectField('Type of Fuel', validators=[InputRequired()],
        choices=[('Petrol', 'Petrol'), ('Electric', 'Electric')])
    submit = SubmitField('Submit')


# -------------------------------
# Form for Bicycle trips
# -------------------------------
class BicycleForm(BaseTripForm):
    fuel_type = SelectField('Type', validators=[InputRequired()],
        choices=[('Standard', 'Standard')])
    submit = SubmitField('Submit')


# -------------------------------
# Form for Walking trips
# -------------------------------
class WalkForm(BaseTripForm):
    fuel_type = SelectField('Type', validators=[InputRequired()],
        choices=[('Standard', 'Standard')])
    submit = SubmitField('Submit')


# -------------------------------
# Form for quick logging a saved trip
# -------------------------------
from wtforms import SelectField
from wtforms.validators import DataRequired

class QuickLogForm(FlaskForm):
    # User selects from a list of previously saved trips (populated in the route)
    trip_id = SelectField('Choose a saved trip', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Log this trip')
