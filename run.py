import threading

from app import create_app, check_urls_periodically

# Create an app instance by calling the create_app function
app = create_app()

if __name__ == '__main__':
    # Start background tasks
    threading.Thread(target=check_urls_periodically, args=(app,), daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

