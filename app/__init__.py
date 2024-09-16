from flask import Flask

app = Flask(__name__)

# Secret key for session management (you can store this in .env)
app.config['SECRET_KEY'] = 'your_secret_key'

# Import routes after app is created to avoid circular imports
from app import routes
