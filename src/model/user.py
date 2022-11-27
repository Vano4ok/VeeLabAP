from src.app import db
from passlib.hash import pbkdf2_sha256 as sha256

from src.model.article import Article
from src.utils.exception_wrapper import handle_error_format


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    articles = db.relationship('Article', backref='user', lazy=True)
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('user', lazy='dynamic'))

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
    def get_by_username_or_id(cls, identifier):
        return User.query.filter((User.email == identifier) | (User.username == identifier)).first()

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'roles': [role.name for role in self.roles],
        }

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)

    @classmethod
    def delete_by_identifier(cls, identifier):
        try:
            user = User.get_by_username_or_id(identifier)

            if not user:
                return handle_error_format('User with such id/username does not exist.',
                                           'Field \'userId/username\' in path parameters.'), 404

            if not user.articles:
                for article in user.articles:
                    Article.delete_note_by_id(article.id)

            user_json = User.to_json(user)
            User.query.filter_by(id=user.id).delete()
            db.session.commit()
            return user_json
        except AttributeError:
            return handle_error_format('User with such id/username does not exist.',
                                       'Field \'userId/username\' in path parameters.'), 404

