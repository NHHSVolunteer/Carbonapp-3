# Flask core imports
from flask import render_template, Blueprint, redirect, url_for, flash, request

# Database models
from Capp.models import Transport, SavedTrip
from Capp import db

# For working with dates
from datetime import timedelta, datetime

# Flask-Login for user session management
from flask_login import current_user

# Import custom forms
from Capp.Carbon_app.forms import (
    BusForm, CarForm, PlaneForm, FerryForm, MotorbikeForm, BicycleForm, WalkForm, TrainForm
)
from Capp.Carbon_app.forms import QuickLogForm

# Create a Blueprint for the carbon app routes
carbon_app = Blueprint('carbon_app', __name__)

# Dictionary: CO₂ emissions per vehicle type in grams per passenger-kilometer (g/pkm)
co2_emissions_per_km = {
    'Plane': {
        'Commercial Airplane': 251    
    },
    'Ferry': {
        'Standard': 123
    },
    'Motorbike': {
        'Small Gasoline Motorbike': 82.77,
        'Medium Gasoline Motorbike': 100.86,
        'Large Gasoline Motorbike': 132.37
    },
    'Car': {
        'Medium Diesel Car': 160,
        'Medium Gasoline Car': 240,
        'Electric SUV': 25,
        'Small Electric Car': 14
    },
    'Bus': {
        'Diesel Bus': 27,
        'Electric Bus' : 13
    },
    'Train' : {
        'Long Range Train': 31,
        'Local Train': 58,
        'Electric Train' : 10,
    },
    'Bicycle': {
        'Standard': 0
    },
    'Walking': {
        'Standard': 0
    }
}

# Convert grams to kilograms and calculate total CO2 emissions
def calculate_emissions_kgs(kms, g_per_km, passengers=1):
    passengers = max(passengers, 1)  # to ensure if no passengers choice, then it is 1
    return round((float(kms) * g_per_km) / (1000 * passengers), 2)

# Reusable function to handle form logic and emissions saving
def handle_form_submission(form, transport):
    if form.validate_on_submit():
        # Extract the number of kilometers and fuel type from the form
        kms = form.kms.data
        type = form.type.data

        # Try to get the number of passengers (only relevant for car/motorbike)
        # If the field doesn't exist (e.g., for bus or plane), default to 1
        passengers = getattr(form, 'passengers', None)
        num_passengers = passengers.data if passengers else 1

        # Get the emissions factor (g CO2 per passenger-km)
        g_per_km = co2_emissions_per_km[transport][type]

        # Calculate total CO2 emissions in kilograms, adjusted for number of passengers
        co2 = calculate_emissions_kgs(kms, g_per_km, passengers=num_passengers)

        # Save the transport log entry to the database
        emissions = Transport(
            kms=kms,
            transport=transport,
            type=type,
            passengers=num_passengers,
            co2=co2,    
            total=co2,
            author=current_user
        )
        db.session.add(emissions)

        # If the user wants to save this trip for reuse later
        if getattr(form, "save_trip", False) and form.save_trip.data:
            name = form.trip_name.data.strip()
            if name:
                saved_trip = SavedTrip(
                    trip_name=name,
                    transport=transport,
                    type=type,
                    kms=kms,
                    passengers=passengers,  
                    user_id=current_user.id
                )
                db.session.add(saved_trip)

        # Commit all changes to the database
        db.session.commit()

        # Redirect to the user's data dashboard after submission
        return redirect(url_for('carbon_app.your_data'))

    # If form is not submitted or validation fails, return None to continue rendering the page
    return None



# Homepage for the carbon app
@carbon_app.route('/carbon_app')
def carbon_app_home():
    return render_template('carbon_app/carbon_app.html', title='Carbon App')

# Individual routes for each vehicle entry
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

@carbon_app.route('/carbon_app/new_entry_train', methods=['GET', 'POST'])
def new_entry_train():
    form = TrainForm()
    result = handle_form_submission(form, 'Train')
    return result or render_template('carbon_app/new_entry_train.html', title='New Train Entry', form=form)



# Quick Log: allows the user to quickly log a previously saved trip
@carbon_app.route('/carbon_app/quick_log', methods=['GET', 'POST'])
def quick_log():
    selected_transport = request.args.get('filter_transport')  # Optional filter, e.g. ?filter_transport=Car
    form = QuickLogForm()

    # Filter saved trips for the current user
    query = SavedTrip.query.filter_by(user_id=current_user.id)
    if selected_transport:
        query = query.filter_by(transport=selected_transport)
    trips = query.all()

    # Populate the select field with saved trips
    form.trip_id.choices = [
        (str(t.id), f"{t.trip_name} ({t.transport}, {t.kms} km)") for t in trips
    ]

    # If the user submits the form, log the selected trip
    if form.validate_on_submit():
        selected = SavedTrip.query.get(int(form.trip_id.data))

        # Use stored passenger count, or default to 1 if not available
        num_passengers = selected.passengers if selected.passengers else 1

        # Lookup emissions factor and calculate CO2
        g_per_km = co2_emissions_per_km[selected.transport][selected.type]
        co2 = calculate_emissions_kgs(selected.kms, g_per_km, passengers=num_passengers)

        # Create and save new Transport log
        trip = Transport(
            kms=selected.kms,
            transport=selected.transport,
            type=selected.type,
            passengers=num_passengers,
            co2=co2,
            total=co2,
            author=current_user
        )
        db.session.add(trip)
        db.session.commit()

        return redirect(url_for('carbon_app.your_data'))

    # Populate the filter dropdown with all distinct transport types
    transport_types = db.session.query(SavedTrip.transport) \
        .filter_by(user_id=current_user.id).distinct().all()
    transport_types = sorted({t[0] for t in transport_types})

    return render_template(
        'carbon_app/quick_log.html',
        title='Quick Log',
        form=form,
        transport_types=transport_types,
        selected_transport=selected_transport
    )

# View logged data (last 5 days only)
@carbon_app.route('/carbon_app/your_data')
def your_data():
    entries = Transport.query.filter_by(author=current_user) \
        .filter(Transport.date > datetime.now() - timedelta(days=5)) \
        .order_by(Transport.date.desc(), Transport.transport.asc()) \
        .all()
    return render_template('carbon_app/your_data.html', title='Your Data', entries=entries)

# Route to delete a specific emission entry
@carbon_app.route('/carbon_app/delete-emission/<int:entry_id>')
def delete_emission(entry_id):
    entry = Transport.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for('carbon_app.your_data'))
