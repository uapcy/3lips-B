from flask import Flask
from api.routes import api_bp  # Import the merged routes

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')  # Register API routes

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app
