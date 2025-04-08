from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired

class BusForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Bus type', [InputRequired()], 
        choices=[
            ('City bus', 'City bus'), 
            ('Coach (long-distance)', 'Coach (long-distance)')
        ])
    submit = SubmitField('Submit')

class CarForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Fuel type', [InputRequired()], 
        choices=[
            ('Petrol', 'Petrol'), 
            ('Diesel', 'Diesel'), 
            ('Electric', 'Electric'),
            ('Hybrid', 'Hybrid')
        ])
    submit = SubmitField('Submit')

class PlaneForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Flight type', [InputRequired()], 
        choices=[
            ('Short-haul flight (≤1,500 km)', 'Short-haul flight (≤1,500 km)'),
            ('Medium-haul flight (1,500–4,000 km)', 'Medium-haul flight (1,500–4,000 km)'),
            ('Long-haul flight (>4,000 km)', 'Long-haul flight (>4,000 km)')
        ])
    submit = SubmitField('Submit')

class FerryForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Passenger type', [InputRequired()], 
        choices=[
            ('Foot passenger', 'Foot passenger'), 
            ('With car', 'With car')
        ])
    submit = SubmitField('Submit')

class MotorbikeForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Engine type', [InputRequired()], 
        choices=[
            ('Petrol', 'Petrol'), 
            ('Electric', 'Electric')
        ])
    submit = SubmitField('Submit')

class BicycleForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Type', [InputRequired()], 
        choices=[
            ('Standard', 'Standard')
        ])
    submit = SubmitField('Submit')

class WalkForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Type', [InputRequired()], 
        choices=[
            ('Standard', 'Standard')
        ])
    submit = SubmitField('Submit')
