import threading

from flask import request, render_template, redirect, url_for, flash, jsonify, abort
from app.forms import URLForm, SearchForm
from app.db_map import URLs, ScrapedData, AlphabetizedData
from app.db import db
#import KWIC.KWIC2
import KWIC.KWIC3
from app.web_scraper import Web_Scraper
from sqlalchemy import or_, not_, and_
import validators
import requests

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

            # Validate the URL
            if not validators.url(url):
                flash('Invalid URL. Please enter a valid URL.', 'danger')
                return redirect(url_for('add_url_to_database'))
            # Ping the URL to check if it's reachable
            try:
                # Set timeout to 5 seconds
                response = requests.get(url, timeout=5) 
                if response.status_code != 200:
                    flash('The URL is not reachable. Please enter a working URL.', 'danger')
                    return redirect(url_for('add_url_to_database'))
            except requests.RequestException:
                flash('The URL is not reachable. Please enter a working URL.', 'danger')
                return redirect(url_for('add_url_to_database'))
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
        print("Circular shift time")
        # Create an instance of Master_Control
        master = KWIC.KWIC3.Master_Control(app)

        # Run the KWIC engine in a separate thread
        process_thread = threading.Thread(target=master.run)
        process_thread.start()

        # Render the initial template
        return render_template('output.html')

    @app.route('/get_records', methods=['GET'])
    def get_records():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Calculate the offset for pagination
        offset = (page - 1) * per_page

        # Retrieve records from the database in the specified page
        with app.app_context():
            batch_records = db.session.query(AlphabetizedData).order_by(AlphabetizedData.text_line).offset(offset).limit(per_page).all()
            records = [record.text_line for record in batch_records]

        return jsonify(records)




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
        message = None
        if form.validate_on_submit():
            keyword = form.keyword.data.strip()
            search_type = form.search_type.data
            case_sensitive = form.case_sensitive.data
            if keyword:
                query = db.session.query(
                    AlphabetizedData.alpha_id,
                    AlphabetizedData.text_line,
                    URLs.search_term,
                    URLs.url
                ).join(URLs, AlphabetizedData.url_id == URLs.url_id)
                
                keywords = keyword.split()
                
                def make_filter(kw):
                    if case_sensitive:
                        return or_(
                            AlphabetizedData.text_line.like(f'% {kw} %'),  # Word between spaces
                            AlphabetizedData.text_line.like(f'{kw} %'),  # Word at the start
                            AlphabetizedData.text_line.like(f'% {kw}'),  # Word at the end
                            AlphabetizedData.text_line == kw,  # Exact match
                            URLs.search_term.like(f'% {kw} %'),
                            URLs.search_term.like(f'{kw} %'),
                            URLs.search_term.like(f'% {kw}'),
                            URLs.search_term == kw
                        )
                    else:
                        return or_(
                            AlphabetizedData.text_line.ilike(f'% {kw} %'),  # Word between spaces
                            AlphabetizedData.text_line.ilike(f'{kw} %'),  # Word at the start
                            AlphabetizedData.text_line.ilike(f'% {kw}'),  # Word at the end
                            AlphabetizedData.text_line.ilike(f'% {kw}'),  # Word at the end
                            URLs.search_term.ilike(f'% {kw} %'),
                            URLs.search_term.ilike(f'{kw} %'),
                            URLs.search_term.ilike(f'% {kw}')
                        )
                
                if search_type == 'and':
                    and_filters = [make_filter(kw) for kw in keywords]
                    query = query.filter(and_(*and_filters))
                elif search_type == 'or':
                    or_filters = [make_filter(kw) for kw in keywords]
                    query = query.filter(or_(*or_filters))
                elif search_type == 'not':
                    not_filters = [make_filter(kw) for kw in keywords]
                    query = query.filter(not_(or_(*not_filters)))
                
                # Order by mfa
                query = query.order_by(AlphabetizedData.mfa.desc())
                # Execute the query and ensure unique URLs
                for result in query.all():
                    url = result.url
                    if url not in results:
                        results[url] = result

            # Check if results are empty
            if results:
                message = None  # Set to None or empty if results are found
            else:
                message = "No results found for your search."

        return render_template('search.html', form=form, results=results.values(), message=message)
        # return render_template('search.html', form=form, results=results.values())




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

    @app.route('/view_user_manual', methods=['GET'])
    def view_user_manual():
        return render_template('view_user_manual.html')


