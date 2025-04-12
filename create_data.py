# Import the application factory and database object
from Capp import create_app, db

# Create the Flask app using the factory function
app = create_app()

# Run everything inside an "app context" to allow DB operations
with app.app_context():
    db.create_all()
    print("Database recreated with passengers in SavedTrip")

