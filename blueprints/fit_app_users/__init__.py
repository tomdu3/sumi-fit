from flask import Flask
from blueprints.fit_app_users.routes import main_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app