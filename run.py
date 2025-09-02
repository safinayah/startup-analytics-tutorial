import os
from app import create_app

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    # Get port from Railway environment variable, default to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app (for local development)
    app.run(
        host='0.0.0.0',  # Listen on all addresses
        port=port,       # Use Railway's port
        debug=False      # Disable debug in production
    )