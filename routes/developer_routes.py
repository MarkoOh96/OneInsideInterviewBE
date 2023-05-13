from flask import Blueprint, jsonify, request
from sqlalchemy import event
from model import db
from models.developers import Developer
from models.projects_developers import ProjectDeveloper

developer_routes = Blueprint('developer_routes', __name__)

@developer_routes.route('/developers', methods=['GET'])
def get_developers():
    developers = Developer.query.all()
    developer_list = [developer.to_dict() for developer in developers]
    return jsonify(developer_list)

@developer_routes.route('/developers/<int:developer_id>', methods=['GET'])
def get_developer(developer_id):
    developer = Developer.query.get(developer_id)
    if developer:
        return jsonify(developer.to_dict())
    return jsonify({'message': 'not found'}), 404

@developer_routes.route('/developers/<string:name>', methods=['GET'])
def get_developer_by_name(name):
    developers = Developer.query.filter(Developer.name.startswith(name)).all()
    developers_list = [developer.to_dict() for developer in developers]
    return jsonify(developers_list)

@developer_routes.route('/developers', methods=['POST'])
def create_developer():
    data = request.get_json()
    developer = Developer(name = data.get('name'), position = data.get('position'))
    db.session.add(developer)
    db.session.commit()
    return jsonify(developer.to_dict()), 201

@developer_routes.route('/developers/<int:developer_id>', methods=['PUT'])
def update_developer(developer_id):
    developer = Developer.query.get(developer_id)
    if developer:
        data = request.get_json()
        developer.name = data.get('name', developer.name)
        developer.position = data.get('position', developer.position)
        db.session.commit()
        return jsonify(developer.to_dict())          
    return jsonify({'message': 'developer not found'}), 404

@developer_routes.route('/developers/<int:developer_id>', methods=['DELETE'])
def delete_developer(developer_id):
    developer = Developer.query.get(developer_id)
    if developer:
        db.session.delete(developer)
        db.session.commit()
        return jsonify({'message': 'developer deleted'})
    return jsonify({'message': 'developer not found'}), 404

@event.listens_for(Developer, 'after_delete')
def delete_records_from_projects_developers(mapper, connection, target):
    ProjectDeveloper.query.filter_by(developer_id=target.id).delete()