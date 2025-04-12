# Import modules needed for database setup and user authentication
from Capp import db, login_manager
from datetime import datetime
from flask_login import UserMixin  # Provides default implementations for Flask-Login

# This function is used by Flask-Login to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch the user from the database by ID

# Define the User model (accounts table)
class User(db.Model, UserMixin):
    __tablename__ = "user_table"  # Explicit name for the table in the database

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(30), unique=True, nullable=False)  # Username must be unique
    email = db.Column(db.String(120), unique=True, nullable=False)    # Email must be unique
    password = db.Column(db.String(60), nullable=False)               # Hashed password

    # Relationship to link this user to their logged trips
    transport = db.relationship('Transport', backref='author', lazy=True)

    # Relationship to link this user to their saved trip templates
    saved_trips = db.relationship('SavedTrip', backref='author', lazy=True)

# Define the Transport model (logs of carbon-emitting trips)
class Transport(db.Model):
    __bind_key__ = 'transport'           # Use the transport-specific database
    __tablename__ = 'transport_table'    # Explicit table name

    id = db.Column(db.Integer, primary_key=True)  # Unique trip ID
    kms = db.Column(db.Float)                     # Number of kilometers traveled
    transport = db.Column(db.String)              # Transport mode (e.g., Bus, Car)
    type = db.Column(db.String)                   # Transport type (Variation of chosen transportation)
    passengers = db.Column(db.Integer, default=1) # Passengers
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Auto-set date
    co2 = db.Column(db.Float)                     # CO₂ emissions in kg
    total = db.Column(db.Float)                   # Total emissions (currently same as CO₂)

    # Link each trip to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)

# Define the SavedTrip model (trip templates that users can quickly log again)
class SavedTrip(db.Model):
    __tablename__ = 'saved_trip'  # Table name

    id = db.Column(db.Integer, primary_key=True)          # Unique ID for the saved trip
    trip_name = db.Column(db.String(100), nullable=False) # Name given by user (e.g., "Home to Work")
    transport = db.Column(db.String(50), nullable=False)  # Type of transport
    type = db.Column(db.String(50), nullable=False)       # Type of chosen transportation
    kms = db.Column(db.Float, nullable=False)             # Distance
    passengers = db.Column(db.Integer, nullable=True)     # Passengers
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)  # Linked user
