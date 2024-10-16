import threading

from flask import request, render_template, redirect, url_for, flash, jsonify
from app.forms import URLForm
from app.db_map import URLs, ScrapedData, AlphabetizedData
from app.db import db
#import KWIC.KWIC2
import KWIC.KWIC3
from app.web_scraper import Web_Scraper


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
        master = KWIC.KWIC3.Master_Control(app)

        # Run the KWIC engine in a separate thread
        process_thread = threading.Thread(target=master.run)
        process_thread.start()

        # Wait for the event to signal completion
        #master.done_event.wait()



        

        master.stop_threads()
        process_thread.join()

        # Run the KWIC engine to get the output
        output_data = master.get_output()

        # Render the output in an HTML template
        return render_template('output.html', output_data=output_data)



    @app.route('/scrape_web_pages', methods=['GET', 'POST'])
    def scrape_web_pages():
        try:
            scraper = Web_Scraper()
            scraper.send_scraped_text_to_database()

            #if sucess
            return render_template('scrape_web_pages.html', success=True)

        except Exception as e:
            # If there's an error, log it and pass success=False to the template
            print(f"Error occurred during scraping: {str(e)}")
            return render_template('scrape_web_pages.html', success=False)



        return render_template('scrape_web_pages.html')

    @app.route('/clear_data', methods=['GET', 'POST'])
    def clear_data():
        if request.method == 'POST':
            try:
                # Delete all rows from AlphabetizedData and ScrapedData using SQLAlchemy's ORM
                db.session.query(AlphabetizedData).delete()
                db.session.query(ScrapedData).delete()

                # Commit the transaction
                db.session.commit()

                flash("Data cleared from AlphabetizedData and ScrapedData tables.", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}", "danger")

            # Redirect to the clear_data page to show a confirmation message
            return redirect(url_for('clear_data'))

        # Render the clear_data template if it's a GET request
        return render_template('clear_data.html')

