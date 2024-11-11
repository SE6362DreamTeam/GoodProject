from app import create_app

# Create an app instance by calling the create_app function
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)
