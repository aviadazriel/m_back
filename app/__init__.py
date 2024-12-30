# from flask import Flask
# # from flask_sqlalchemy import SQLAlchemy
# import os
#
# # db = SQLAlchemy()
#
#
# def create_app():
#     app = Flask(__name__)
#
#     # Load configuration
#     app.config.from_object('app.config.Config')
#
#     # Initialize extensions
#     db.init_app(app)
#
#     # Ensure upload folder exists
#     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#
#     # Import and register blueprints
#     from app.routes import main
#     app.register_blueprint(main)
#
#     return app
