from flask import Blueprint, jsonify, request
from sqlalchemy import event
from model import db
from models.clients import Client
from models.projects import Project
from models.projects_developers import ProjectDeveloper

project_routes = Blueprint('project_routes', __name__)

@project_routes.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    project_list = [project.to_dict() for project in projects]
    return jsonify(project_list)

@project_routes.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get(project_id)
    if project:
        return jsonify(project.to_dict())
    return jsonify({'message': 'not found'}), 404

@project_routes.route('/projects/<string:name>', methods=['GET'])
def get_project_by_name(name):
    projects = Project.query.filter(Project.name.startswith(name)).all()
    projects_list = [project.to_dict() for project in projects]
    return jsonify(projects_list)

@project_routes.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    client = Client.query.filter_by(name = data.get('client')).first()
    print(data)
    if not client:
        client = Client(name = data.get('client'), info = "")
        db.session.add(client)
        db.session.commit()

    project = Project(name = data.get('name'), country = data.get('country'), client = client)
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201
    

@project_routes.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get(project_id)
    if project:
        data = request.get_json()
        project.name = data.get('name', project.name)
        project.country = data.get('country', project.country)
        client = Client.query.filter_by(name = data.get('client')).first()
        if client:
            project.client = client
        db.session.commit()
        return jsonify(project.to_dict())
    return jsonify({'message': 'project not found'}), 404

@project_routes.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = project.query.get(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'project deleted'})
    return jsonify({'message': 'project not found'}), 404

@event.listens_for(Project, 'after_delete')
def delete_records_from_projects_projects(mapper, connection, target):
    ProjectDeveloper.query.filter_by(project_id=target.id).delete()