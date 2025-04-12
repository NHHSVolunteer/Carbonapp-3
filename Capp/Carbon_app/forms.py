# Import base class for forms in Flask
from flask_wtf import FlaskForm

# Import commonly used field types and validators
from wtforms import SubmitField, SelectField, FloatField, BooleanField, StringField, IntegerField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, DataRequired

# -------------------------------
# Base class for shared form logic
# -------------------------------
class BaseTripForm(FlaskForm):
    kms = FloatField('Kilometers', validators=[InputRequired()])
    save_trip = BooleanField('Save this trip?')
    trip_name = StringField('Trip Name (if saving)', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Submit')  # Included in base so child classes don't need to redefine it


# -------------------------------
# Form for Bus trips
# -------------------------------
class BusForm(BaseTripForm):
    fuel_type = SelectField(
        'Type of Fuel',
        validators=[InputRequired()],
        choices=[
            ('Diesel', 'Diesel'),
            ('CNG', 'CNG'),
            ('Petrol', 'Petrol'),
            ('No Fossil Fuel', 'No Fossil Fuel')
        ]
    )


# -------------------------------
# Form for Car trips
# -------------------------------
class CarForm(BaseTripForm):
    fuel_type = SelectField(
        'Type of Fuel',
        validators=[InputRequired()],
        choices=[
            ('Medium Diesel Car', 'Medium Diesel Car'),
            ('Medium Gasoline Car', 'Medium Gasoline Car'),
            ('Electric SUV', 'Electric SUV'),
            ('Small Electric Car', 'Small Electric Car')
        ]
    )
    passengers = IntegerField(
        'Number of Passengers (including yourself)',
        validators=[InputRequired(), NumberRange(min=1, max=8)]
    )


# -------------------------------
# Form for Plane trips
# -------------------------------
class PlaneForm(BaseTripForm):
    fuel_type = SelectField(
        'Flight Type',
        validators=[InputRequired()],
        choices=[
            ('Short-haul flight (≤1,500 km)', 'Short-haul flight (≤1,500 km)'),
            ('Medium-haul flight (1,500–4,000 km)', 'Medium-haul flight (1,500–4,000 km)'),
            ('Long-haul flight (>4,000 km)', 'Long-haul flight (>4,000 km)')
        ]
    )


# -------------------------------
# Form for Ferry trips
# -------------------------------
class FerryForm(BaseTripForm):
    fuel_type = SelectField(
        'Passenger Type',
        validators=[InputRequired()],
        choices=[
            ('Foot passenger', 'Foot passenger'),
            ('With car', 'With car')
        ]
    )


# -------------------------------
# Form for Motorbike trips
# -------------------------------
class MotorbikeForm(BaseTripForm):
    fuel_type = SelectField(
        'Type of Fuel',
        validators=[InputRequired()],
        choices=[
            ('Petrol', 'Petrol'),
            ('Electric', 'Electric')
        ]
    )
    passengers = IntegerField(
        'Number of Passengers (including yourself)',
        validators=[InputRequired(), NumberRange(min=1, max=2)]
    )


# -------------------------------
# Form for Bicycle trips
# -------------------------------
class BicycleForm(BaseTripForm):
    fuel_type = SelectField(
        'Type',
        validators=[InputRequired()],
        choices=[('Standard', 'Standard')]
    )


# -------------------------------
# Form for Walking trips
# -------------------------------
class WalkForm(BaseTripForm):
    fuel_type = SelectField(
        'Type',
        validators=[InputRequired()],
        choices=[('Standard', 'Standard')]
    )


# -------------------------------
# Form for quick logging a saved trip
# -------------------------------
class QuickLogForm(FlaskForm):
    trip_id = SelectField('Choose a saved trip', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Log this trip')
