from flask import Blueprint, jsonify, request
from sqlalchemy import event
from model import db
from models.projects_developers import ProjectDeveloper
from models.projects import Project
from models.developers import Developer

project_developer_routes = Blueprint('project_developer_routes', __name__)


@project_developer_routes.route('/developers_by_project/<int:project_id>', methods=['GET'])
def get_developers(project_id):   
    query = db.session.query(ProjectDeveloper, Developer).join(Developer).filter(ProjectDeveloper.project_id == project_id).all()
    results = []
    for pd, developer in query:
        results.append(developer.to_dict())
    return jsonify(results), 200

@project_developer_routes.route('/project_developer', methods=['GET'])
def get_all_developers():   
    developers = ProjectDeveloper.query.all()
    developer_list = [developer.to_dict() for developer in developers]
    return jsonify(developer_list)

@project_developer_routes.route('/projects_by_developer/<int:developer_id>', methods=['GET'])
def get_projects(developer_id):
    projects = ProjectDeveloper.query.filter_by(developer_id = developer_id).all()
    projects_list = [project.to_dict() for project in projects]
    if projects_list:
        return jsonify(projects_list)
    return jsonify({'message': 'not found'}), 404

@project_developer_routes.route('/project_developers', methods=['POST'])
def create_project_developer():
    data = request.get_json()
    project = Project.query.get(data.get('project_id'))
    developer = Developer.query.get(data.get('developer_id'))
    if project and developer:
        project_developer = ProjectDeveloper(project = project, developer = developer)
        db.session.add(project_developer)
        db.session.commit()
        print(developer.to_dict())
        return jsonify(developer.to_dict()), 201
    return jsonify({'message': 'not found'}), 404


@project_developer_routes.route('/project-developers/<int:project_id>/<int:developer_id>', methods=['DELETE'])
def deleteDeveloperFromProject(project_id, developer_id):
    project_developer = ProjectDeveloper.query.get((project_id, developer_id))
    if project_developer:
        db.session.delete(project_developer)
        db.session.commit()

        return jsonify({'message': 'ProjectDeveloper record deleted successfully.'}), 200
    else:
        return jsonify({'error': 'ProjectDeveloper record not found.'}), 404

