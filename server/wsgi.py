from app import app  # Import the Flask application instance created in the 'app' module.

# This block checks if the script is being run directly (not imported as a module).
if __name__ == "__main__":
    # Run the app in debug mode.
    # Debug mode provides helpful error messages and auto-reloads the server on code changes.
    app.run(debug=True)
