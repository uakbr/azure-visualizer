from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__)

# Configuration settings for the application
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///azure_permissions_visualizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import views, models

if __name__ == '__main__':
    app.run(debug=True)
