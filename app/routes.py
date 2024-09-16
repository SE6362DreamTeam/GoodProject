from app import app  # Make sure to import your Flask app instance
from flask import render_template, request, redirect, url_for



# Home page route (index)
@app.route('/')
def index():
    return render_template('index.html')

# Add URL to database route
@app.route('/add_url_to_database', methods=['GET', 'POST'])
def add_url_to_database():
    if request.method == 'POST':
        # Here you would process the form submission
        pass
    return render_template('add_url_to_database.html')