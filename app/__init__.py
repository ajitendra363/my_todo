from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)  # <-- make sure this line is exactly here, no indentation issues

    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)   # <-- app must be defined before this

    from app.routes.auth import auth_bp
    from app.routes.task import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
