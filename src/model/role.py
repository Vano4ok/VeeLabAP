from src.app import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
