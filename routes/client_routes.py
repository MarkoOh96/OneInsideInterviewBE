from flask import Blueprint, jsonify, request
from model import db
from models.clients import Client

client_routes = Blueprint('client_routes', __name__)

@client_routes.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    client_list = [client.to_dict() for client in clients]
    return jsonify(client_list)

@client_routes.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if client:
        return jsonify(client.to_dict())
    return jsonify({'message': 'not found'}), 404

@client_routes.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    client = Client(name = data.get('name'), info = data.get('info'), img = data.get('img'))
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

@client_routes.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted'})
    return jsonify({'message': 'Client not found'}), 404