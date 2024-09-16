from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import URLForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_url_to_database', methods=['GET', 'POST'])
def add_url_to_database():
    form = URLForm()
    if form.validate_on_submit():
        # Handle form submission logic here
        flash(f'URL added: {form.url.data} with search term: {form.search_term.data}', 'success')
        return redirect(url_for('index'))
    return render_template('add_url_to_database.html', form=form)
