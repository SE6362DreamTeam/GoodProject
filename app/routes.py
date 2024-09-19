import threading

from flask import render_template, redirect, url_for, flash
from app.forms import URLForm
from app.db_map import URLs
from app.db import db
import KWIC.KWIC2


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

            try:
                # Add the new URL to the database
                db.session.add(new_url)
                db.session.commit()
                flash('URL added successfully!', 'success')
            except Exception as e:
                db.session.rollback()  # Rollback in case of an error
                flash(f'Error: {str(e)}', 'danger')

            return redirect(url_for('add_url_to_database'))

        # Query all URLs using session.query
        urls = db.session.query(URLs).all()

        # Render the form template and pass the URLs to the template
        return render_template('add_url_to_database.html', form=form, urls=urls)








    @app.route('/circular_shift_demo', methods=['GET', 'POST'])
    def circular_shift_demo():

        # Create an instance of Master_Control
        master = KWIC.KWIC2.Master_Control()

        # Run the KWIC engine in a separate thread
        process_thread = threading.Thread(target=master.run)
        process_thread.start()

        # Wait for the event to signal completion
        #master.done_event.wait()



        # Run the KWIC engine to get the output
        output_data = master.get_output()

        # If output_data is not a list, convert it to one
        if isinstance(output_data, str):
            output_data = output_data.split('\n')

        # If it's empty or None, provide a default message
        if not output_data:
            output_data = ["No output data generated"]

        # Render the output in an HTML template
        return render_template('output.html', output_data=output_data)





