from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField, BooleanField, StringField, IntegerField
from wtforms.validators import InputRequired, Optional, Length, NumberRange, DataRequired

# -------------------------------
# Base class for shared fields
# -------------------------------
class BaseTripForm(FlaskForm):
    kms = FloatField('Kilometers', validators=[InputRequired()])
    save_trip = BooleanField('Save this trip?')
    trip_name = StringField('Trip Name (if saving)', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Submit')  # All forms inherit this


# -------------------------------
# Form for Bus trips
# -------------------------------
class BusForm(BaseTripForm):
    type = SelectField(
        'Type of Bus',
        validators=[InputRequired()],
        choices=[
            ('Diesel Bus', 'Diesel Bus'),
            ('Electric Bus', 'Electric Bus')
        ]
    )


# -------------------------------
# Form for Car trips
# -------------------------------
class CarForm(BaseTripForm):
    type = SelectField(
        'Car Type',
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
    type = SelectField(
        'Flight Type',
        validators=[InputRequired()],
        choices=[
            ('Commercial Airplane', 'Commercial Airplane')
        ]
    )


# -------------------------------
# Form for Ferry trips
# -------------------------------
class FerryForm(BaseTripForm):
    type = SelectField(
        'Ferry Type',
        validators=[InputRequired()],
        choices=[
            ('Standard', 'Standard')
        ]
    )


# -------------------------------
# Form for Motorbike trips
# -------------------------------
class MotorbikeForm(BaseTripForm):
    type = SelectField(
        'Motorbike Type',
        validators=[InputRequired()],
        choices=[
            ('Small Gasoline Motorbike', 'Small Gasoline Motorbike'),
            ('Medium Gasoline Motorbike', 'Medium Gasoline Motorbike'),
            ('Large Gasoline Motorbike', 'Large Gasoline Motorbike')
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
    type = SelectField(
        'Type',
        validators=[InputRequired()],
        choices=[('Standard', 'Standard')]
    )


# -------------------------------
# Form for Walking trips
# -------------------------------
class WalkForm(BaseTripForm):
    type = SelectField(
        'Type',
        validators=[InputRequired()],
        choices=[('Standard', 'Standard')]
    )

# -------------------------------
# Form for Train trips
# -------------------------------
class TrainForm(BaseTripForm):
    type = SelectField(
        'Train Type',
        validators=[InputRequired()],
        choices=[
            ('Long Range Train', 'Long Range Train'),
            ('Local Train', 'Local Train'),
            ('Electric Train', 'Electric Train')
        ]
    )


# -------------------------------
# Form for quick logging a saved trip
# -------------------------------
class QuickLogForm(FlaskForm):
    trip_id = SelectField('Choose a saved trip', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Log this trip')
