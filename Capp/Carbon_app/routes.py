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
        # Extract the number of kilometers and type from the form
        kms = form.kms.data
        type = form.type.data

        # Get the number of passengers if available (relevant for car/motorbike only)
        passengers = getattr(form, 'passengers', None)
        num_passengers = passengers.data if passengers else 1

        # Lookup CO2 emissions per km per passenger
        g_per_km = co2_emissions_per_km[transport][type]

        # Calculate total CO2 emissions
        co2 = calculate_emissions_kgs(kms, g_per_km, passengers=num_passengers)

        # Save this entry to the Transport table
        emissions = Transport(
            kms=kms,
            transport=transport,
            type=type,
            passengers=num_passengers,
            co2=co2,
            author=current_user
        )
        db.session.add(emissions)

        # Save trip for quick log if checkbox is checked and trip name is valid
        if getattr(form, "save_trip", False) and form.save_trip.data:
            name = form.trip_name.data.strip()
            if name:
                saved_trip = SavedTrip(
                    trip_name=name,
                    transport=transport,
                    type=type,
                    kms=kms,
                    passengers=num_passengers,
                    user_id=current_user.id
                )
                db.session.add(saved_trip)

        # Commit everything to the database
        db.session.commit()

        # Comparison values for jeans and beef
        jeans_eq = round(co2 / 33, 2)   # 33 kg CO₂ per pair of jeans src: 
        beef_eq = round(co2 / 27, 2)    # 27 kg CO₂ per kg beef src: 

        # Create a comparison message
        comparison_message = (
            f"Your trip emitted {co2} kg CO₂, which is equivalent to producing "
            f"{jeans_eq} pair(s) of jeans or {beef_eq} kg of beef."
        )

        # Flash the comparison to the user
        flash(comparison_message, 'info')

        # Redirect to dashboard
        return redirect(url_for('carbon_app.your_data'))

    # Form not submitted or has validation errors
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


@carbon_app.route('/carbon_app/quick_log', methods=['GET', 'POST'])
def quick_log():
    # Filter to only show trips of a specific transport type
    selected_transport = request.args.get('filter_transport')
    form = QuickLogForm()

    # Fetch saved trips for the logged-in user, filtered if specified
    query = SavedTrip.query.filter_by(user_id=current_user.id)
    if selected_transport:
        query = query.filter_by(transport=selected_transport)
    trips = query.all()

    # Populate the dropdown with saved trip options
    form.trip_id.choices = [
        (str(t.id), f"{t.trip_name} ({t.transport}, {t.kms} km)") for t in trips
    ]

    # If the form is submitted and valid, proceed to log the trip
    if form.validate_on_submit():
        # Get the selected saved trip from the database
        selected = SavedTrip.query.get(int(form.trip_id.data))

        # Use stored passenger count or default to 1 if not set
        num_passengers = selected.passengers if selected.passengers else 1

        # Look up emissions factor for this transport type
        g_per_km = co2_emissions_per_km[selected.transport][selected.type]

        # Calculate the total CO₂ emissions for this trip
        co2 = calculate_emissions_kgs(selected.kms, g_per_km, passengers=num_passengers)

        # Save a new transport entry based on the saved trip
        trip = Transport(
            kms=selected.kms,
            transport=selected.transport,
            type=selected.type,
            passengers=num_passengers,
            co2=co2,
            author=current_user
        )
        db.session.add(trip)
        db.session.commit()

        # Create a helpful comparison message for the user
        jeans_eq = round(co2 / 33, 2)  # Average emissions to make one pair of jeans
        beef_eq = round(co2 / 27, 2)   # Average emissions to produce one kg of beef

        comparison_message = (
            f"Your trip emitted {co2} kg CO₂, which is equivalent to producing "
            f"{jeans_eq} pair(s) of jeans or {beef_eq} kg of beef."
        )

        # Display the message as a flash alert
        flash(comparison_message, 'info')

        # Redirect the user to their dashboard
        return redirect(url_for('carbon_app.your_data'))

    # For the dropdown menu: get distinct transport types for this user
    transport_types = db.session.query(SavedTrip.transport) \
        .filter_by(user_id=current_user.id).distinct().all()
    transport_types = sorted({t[0] for t in transport_types})

    # Render the quick log page
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
