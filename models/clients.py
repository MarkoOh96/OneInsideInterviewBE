from model import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'img': self.img
        }