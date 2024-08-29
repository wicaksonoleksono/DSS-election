from flask import Flask
import firebase_admin
from firebase_admin import credentials
from controllers.saw_controller import saw_bp
from controllers.wp_controller import wp_bp

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("FirebaseCred.json")
firebase_admin.initialize_app(cred)

# Register Blueprints for SAW and WP
app.register_blueprint(saw_bp, url_prefix="/saw")
app.register_blueprint(wp_bp, url_prefix="/wp")

if __name__ == "__main__":
    app.run(debug=True)
