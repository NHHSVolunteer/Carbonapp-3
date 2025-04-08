from flask import render_template, Blueprint, redirect, url_for, flash
from Capp.models import Transport
from Capp import db
from datetime import timedelta, datetime
from flask_login import current_user
from Capp.Carbon_app.forms import BusForm, CarForm, PlaneForm, FerryForm, MotorbikeForm, BicycleForm, WalkForm

carbon_app = Blueprint('carbon_app', __name__)

# CO₂ emissions in grams per passenger-kilometer (g/pkm)
co2_emissions_per_km = {
    'Plane': {
        'Short-haul flight (≤1,500 km)': 251,
        'Medium-haul flight (1,500–4,000 km)': 195,
        'Long-haul flight (>4,000 km)': 150
    },
    'Ferry': {
        'Foot passenger': 19,
        'With car': 130
    },
    'Motorbike': {
        'Petrol': 83,
        'Electric': 0
    },
    'Car': {
        'Petrol': 170,
        'Diesel': 173,
        'Electric': 47,
        'Hybrid': 121
    },
    'Bus': {
        'City bus': 90,
        'Coach (long-distance)': 27
    },
    'Bicycle': {
        'Standard': 0
    },
    'Walking': {
        'Standard': 0
    }
}

def calculate_emissions_kgs(kms, g_per_km):
    return round((float(kms) * g_per_km) / 1000, 2)

def handle_form_submission(form, transport):
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        g_per_km = co2_emissions_per_km[transport][fuel]
        co2 = calculate_emissions_kgs(kms, g_per_km)
        emissions = Transport(
            kms=kms,
            transport=transport,
            fuel=fuel,
            co2=co2,
            ch4=0.0,
            total=co2,
            author=current_user
        )
        db.session.add(emissions)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return None

@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='carbon_app')

@carbon_app.route('/carbon_app/new_entry_bus', methods=['GET', 'POST'])
def new_entry_bus():
    form = BusForm()
    result = handle_form_submission(form, 'Bus')
    return result or render_template('carbon_app/new_entry_bus.html', title='New Bus Entry', form=form)

@carbon_app.route('/carbon_app/new_entry_car', methods=['GET', 'POST'])
def new_entry_car():
    form = CarForm()
    result = handle_form_submission(form, 'Car')
    return result or render_template('carbon_app/new_entry_car.html', title='New Car Entry', form=form)

@carbon_app.route('/carbon_app/new_entry_plane', methods=['GET', 'POST'])
def new_entry_plane():
    form = PlaneForm()
    result = handle_form_submission(form, 'Plane')
    return result or render_template('carbon_app/new_entry_plane.html', title='New Plane Entry', form=form)

@carbon_app.route('/carbon_app/new_entry_ferry', methods=['GET', 'POST'])
def new_entry_ferry():
    form = FerryForm()
    result = handle_form_submission(form, 'Ferry')
    return result or render_template('carbon_app/new_entry_ferry.html', title='New Ferry Entry', form=form)

@carbon_app.route('/carbon_app/new_entry_motorbike', methods=['GET', 'POST'])
def new_entry_motorbike():
    form = MotorbikeForm()
    result = handle_form_submission(form, 'Motorbike')
    return result or render_template('carbon_app/new_entry_motorbike.html', title='New Motorbike Entry', form=form)

@carbon_app.route('/carbon_app/new_entry_bicycle', methods=['GET', 'POST'])
def new_entry_bicycle():
    form = BicycleForm()
    result = handle_form_submission(form, 'Bicycle')
    return result or render_template('carbon_app/new_entry_bicycle.html', title='New Bicycle Entry', form=form)

@carbon_app.route('/carbon_app/new_entry_walk', methods=['GET', 'POST'])
def new_entry_walk():
    form = WalkForm()
    result = handle_form_submission(form, 'Walking')
    return result or render_template('carbon_app/new_entry_walk.html', title='New Walk Entry', form=form)

@carbon_app.route('/carbon_app/your_data')
def your_data():
    entries = Transport.query.filter_by(author=current_user) \
        .filter(Transport.date > datetime.now() - timedelta(days=5)) \
        .order_by(Transport.date.desc(), Transport.transport.asc()) \
        .all()
    return render_template('carbon_app/your_data.html', title='Your Data', entries=entries)

@carbon_app.route('/carbon_app/delete-emission/<int:entry_id>')
def delete_emission(entry_id):
    entry = Transport.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for('carbon_app.your_data'))
