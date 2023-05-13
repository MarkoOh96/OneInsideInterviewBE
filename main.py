from flask import Flask, jsonify
from model import db
from routes.client_routes import client_routes
from routes.developer_routes import developer_routes
from routes.project_routes import project_routes
import requests
from models.clients import Client
from models.developers import Developer
from models.projects import Project
from models.projects_developers import ProjectDeveloper


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db.init_app(app)

app.register_blueprint(client_routes)
app.register_blueprint(developer_routes)
app.register_blueprint(project_routes)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

    response = requests.post(Base + 'clients', jsonify(client))