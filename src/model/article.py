from src.app import db
from strenum import StrEnum
from sqlalchemy import func
from sqlalchemy import DateTime, Enum

from src.utils.exception_wrapper import handle_error_format


class State(StrEnum):
    NEW = 'New'
    IN_REVIEW = 'In Review'
    CONFIRMED = 'Confirmed'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.String(700), nullable=False)
    date = db.Column(DateTime(timezone=True), server_default=func.now())
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    state = db.Column(Enum(State), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            'title': self.title,
            'text': self.text,
            'date': self.date,
            'userId': self.userId,
            'state': self.state
        }

    @classmethod
    def get_by_id(cls, article_id):
        return cls.query.filter_by(id=article_id).first()

    @classmethod
    def get_all(cls):
        return {'articles': [cls.to_json(article) for article in Article.query.all()]}

    @classmethod
    def delete_by_id(cls, article_id):
        article = Article.get_by_id(article_id)

        if not article:
            return handle_error_format('Article with such id does not exist.',
                                       'Field \'articleId\' in path parameters.'), 404

        article_json = article.to_json()

        cls.query.filter_by(id=article_id).delete()
        db.session.commit()

        return article_json
