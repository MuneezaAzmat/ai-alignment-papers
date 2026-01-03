#!/usr/bin/env python3
from app import create_app
from scheduler import start_scheduler
import os

app = create_app()

# Start the background scheduler
scheduler = start_scheduler()

if __name__ == '__main__':
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
