from flask import Flask
from model import db
from models.clients import Client
from models.developers import Developer
from models.projects import Project
from models.projects_developers import ProjectDeveloper


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)