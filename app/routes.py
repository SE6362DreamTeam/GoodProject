from flask import render_template, redirect, url_for, flash
from app.forms import URLForm
from app.db_map import URLs
from app.db import db


def init_app(app):
    """Function to initialize routes"""

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add_url_to_database', methods=['GET', 'POST'])
    def add_url_to_database():
        form = URLForm()

        if form.validate_on_submit():
            # Get data from the form
            search_term = form.search_term.data
            url = form.url.data

            # Create a new instance of the URLs model
            new_url = URLs(search_term=search_term, url=url)

            # Add the new URL to the database
            db.session.add(new_url)
            db.session.commit()  # Commit the transaction

            # Flash a success message
            flash('URL added successfully!', 'success')

            return redirect(url_for('add_url_to_database'))

        # Render the form template
        return render_template('add_url_to_database.html', form=form)
