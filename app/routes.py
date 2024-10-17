import threading

from flask import request, render_template, redirect, url_for, flash, jsonify, abort
from app.forms import URLForm, SearchForm
from app.db_map import URLs, ScrapedData, AlphabetizedData
from app.db import db
#import KWIC.KWIC2
import KWIC.KWIC3
from app.web_scraper import Web_Scraper
from sqlalchemy import or_, not_, and_


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


        process_thread.join()
        master.stop_threads()

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







    @app.route('/search', methods=['GET', 'POST'])
    def search():
        form = SearchForm()
        results = {}

        if form.validate_on_submit():
            keyword = form.keyword.data.strip()
            search_type = form.search_type.data

            if keyword:
                query = db.session.query(
                    AlphabetizedData.alpha_id,
                    AlphabetizedData.text_line,
                    URLs.search_term,
                    URLs.url
                ).join(URLs, AlphabetizedData.url_id == URLs.url_id)

                keywords = keyword.split()
                if search_type == 'and':
                    # AND search: Each keyword should appear in either field
                    and_filters = [
                        or_(
                            AlphabetizedData.text_line.ilike(f'%{kw}%'),
                            URLs.search_term.ilike(f'%{kw}%')
                        ) for kw in keywords
                    ]
                    query = query.filter(and_(*and_filters))
                elif search_type == 'or':
                    # OR search: Any keyword can be in any field
                    or_filters = [
                        or_(
                            AlphabetizedData.text_line.ilike(f'%{kw}%'),
                            URLs.search_term.ilike(f'%{kw}%')
                        ) for kw in keywords
                    ]
                    query = query.filter(or_(*or_filters))
                elif search_type == 'not':
                    # NOT search: None of the keywords should be in either field
                    not_filters = [
                        or_(
                            AlphabetizedData.text_line.ilike(f'%{kw}%'),
                            URLs.search_term.ilike(f'%{kw}%')
                        ) for kw in keywords
                    ]
                    query = query.filter(not_(or_(*not_filters)))

                # Order by mfa
                query = query.order_by(AlphabetizedData.mfa.desc())

                # Execute the query and ensure unique URLs
                for result in query.all():
                    url = result.url
                    if url not in results:
                        results[url] = result

        return render_template('search.html', form=form, results=results.values())


    #this route is used to access the page and increment the mfa count
    @app.route('/page/<int:alpha_id>')
    def access_page(alpha_id):
        # Query the AlphabetizedData entry by its id
        alpha_entry = db.session.query(AlphabetizedData).get(alpha_id)

        if alpha_entry:
            # Increment the mfa count
            alpha_entry.mfa += 1

            try:
                # Commit the increment to the database
                db.session.commit()
                print(f"Successfully incremented MFA for alpha_id {alpha_id}, new MFA: {alpha_entry.mfa}")
            except Exception as e:
                db.session.rollback()  # Rollback in case of error
                print(f"Failed to increment MFA for alpha_id {alpha_id}: {e}")
                flash("Failed to update click count.", "danger")
                return redirect(url_for('search'))

            # Query the URL associated with this entry
            url_entry = db.session.query(URLs).get(alpha_entry.url_id)
            if url_entry:
                # Redirect to the actual URL
                return redirect(url_entry.url)
            else:
                flash("URL not found.", "danger")
        else:
            flash("Page entry not found.", "danger")

        # Redirect back to search page if entry or URL is missing
        return redirect(url_for('search'))




