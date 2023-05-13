from model import db

class ProjectDeveloper(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    project = db.relationship('Project', backref=db.backref('projects', lazy=True))
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), primary_key=True)
    developer = db.relationship('Developer', backref=db.backref('developers', lazy=True))
    
    def to_dict(self):
        return {
            'project_id': self.project_id,
            'developer_id': self.developer_id,
        }