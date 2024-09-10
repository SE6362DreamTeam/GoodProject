from flask import Flask, render_template, request

app = Flask(__name__)

# Mock database of KWIC-indexed web pages (for demonstration)
database = [
    {"title": "Python Programming", "url": "https://www.python.org", "snippet": "Learn Python programming with this comprehensive guide."},
    {"title": "Flask Web Development", "url": "https://flask.palletsprojects.com/en/3.0.x/", "snippet": "Get started with Flask web development and build powerful web apps."},
    {"title": "Bootstrap for Web Design", "url": "https://getbootstrap.com/", "snippet": "Use Bootstrap to create responsive and beautiful web designs."}
]

@app.route('/', methods=['GET', 'POST'])
def search():
    results = []
    query = ""

    if request.method == 'POST':
        query = request.form['query']
        # Simple search in the mock database (you can replace this with your KWIC search)
        results = [page for page in database if query.lower() in page['title'].lower() or query.lower() in page['snippet'].lower()]

    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
