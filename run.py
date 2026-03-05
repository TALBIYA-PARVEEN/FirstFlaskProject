import os
from app import create_app

# Create the Flask app using your factory function
app = create_app()

if __name__ == '__main__':
    # Get port from environment (Render provides this)
    port = int(os.environ.get('PORT', 5000))
    
    # Detect environment: 'development' or 'production'
    flask_env = os.environ.get('FLASK_ENV', 'development')
    
    # Enable debug only in development
    debug = flask_env == 'development'
    
    # Listen on all network interfaces for Render deployment
    app.run(host='0.0.0.0', port=port, debug=debug)