# Import the create_app function from your Capp package (__init__.py)
from Capp import create_app

# Call the factory function to create a Flask application instance
application = create_app()

# Run the application in development mode with debug enabled
# This means the server will automatically reload if you make changes to the code,
# and it will show detailed error messages in the browser when things go wrong.
if __name__ == '__main__':
    application.run(debug=True)
