from flask import Flask
from app.config import FLASK_SECRET_KEY
import os

def create_app():
    # Get the project root directory (parent of app/)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(__name__,
                template_folder=os.path.join(root_dir, 'templates'),
                static_folder=os.path.join(root_dir, 'static'))
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app
