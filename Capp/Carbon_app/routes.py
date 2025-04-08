from flask import render_template, Blueprint, redirect, url_for, flash, request
from Capp.models import Transport, SavedTrip
from Capp import db
from datetime import timedelta, datetime
from flask_login import current_user
from Capp.Carbon_app.forms import (
    BusForm, CarForm, PlaneForm, FerryForm, MotorbikeForm, BicycleForm, WalkForm
)
from Capp.Carbon_app.forms import QuickLogForm

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
        'Diesel': 90,
        'CNG': 75,
        'Petrol': 90,
        'No Fossil Fuel': 0
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

        # Lagre transportoppførsel
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

        # Hvis brukeren vil lagre denne turen
        if getattr(form, "save_trip", False) and form.save_trip.data:
            name = form.trip_name.data.strip()
            if name:
                saved_trip = SavedTrip(
                    trip_name=name,
                    transport=transport,
                    fuel=fuel,
                    kms=kms,
                    user_id=current_user.id
                )
                db.session.add(saved_trip)

        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))
    return None

@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='Carbon App')

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

@carbon_app.route('/carbon_app/quick_log', methods=['GET', 'POST'])
def quick_log():
    selected_transport = request.args.get('filter_transport')
    form = QuickLogForm()

    query = SavedTrip.query.filter_by(user_id=current_user.id)
    if selected_transport:
        query = query.filter_by(transport=selected_transport)

    trips = query.all()
    form.trip_id.choices = [
        (str(t.id), f"{t.trip_name} ({t.transport}, {t.kms} km)") for t in trips
    ]

    if form.validate_on_submit():
        selected = SavedTrip.query.get(int(form.trip_id.data))
        g_per_km = co2_emissions_per_km[selected.transport][selected.fuel]
        co2 = calculate_emissions_kgs(selected.kms, g_per_km)

        trip = Transport(
            kms=selected.kms,
            transport=selected.transport,
            fuel=selected.fuel,
            co2=co2,
            ch4=0.0,
            total=co2,
            author=current_user
        )
        db.session.add(trip)
        db.session.commit()
        return redirect(url_for('carbon_app.your_data'))

    transport_types = db.session.query(SavedTrip.transport).filter_by(user_id=current_user.id).distinct().all()
    transport_types = sorted({t[0] for t in transport_types})

    return render_template(
        'carbon_app/quick_log.html',
        title='Quick Log',
        form=form,
        transport_types=transport_types,
        selected_transport=selected_transport
    )


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
