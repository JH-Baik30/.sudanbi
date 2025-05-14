# app/__init__.py
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_app():
    app = Flask(__name__)

    engine = create_engine('sqlite:///wordbook.db')
    Session = sessionmaker(bind=engine)
    app.session = Session()

    from .views import main
    app.register_blueprint(main)

    return app
