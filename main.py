from flask import Flask, jsonify
from flask_cors import CORS
from model import db
from routes.client_routes import client_routes
from routes.developer_routes import developer_routes
from routes.project_routes import project_routes
from routes.project_developers_resources import project_developer_routes
import requests


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'

db.init_app(app)

app.register_blueprint(client_routes)
app.register_blueprint(developer_routes)
app.register_blueprint(project_routes)
app.register_blueprint(project_developer_routes)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)

    response = requests.post(Base + 'clients', jsonify(client))