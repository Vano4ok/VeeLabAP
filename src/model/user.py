from src.app import db
from passlib.hash import pbkdf2_sha256 as sha256

from src.model.article import Article


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    articles = db.relationship('Article', backref='user', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def delete_by_id(cls, user_id):
        try:
            user = User.get_by_id(user_id)

            for article in user.articles:
                Article.delete_note_by_id(article.id)

            user_json = User.to_json(user)
            User.query.filter_by(id=user_id).delete()
            db.session.commit()
            return user_json
        except:
            return {'message': 'User with such id does not exist.'}, 404

    def to_json(user):
        return {
            'id': user.id,
            'username': user.username,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'email': user.email,
            'password': user.password
        }

    @classmethod
    def return_all(cls):
        return {'users': [user.to_json() for user in User.query.all()]}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)
