from src.app import app
from src.model.user import User
from src.model.article import State, Article
from flask_restful import reqparse

from src.utils.exception_wrapper import handle_error_format


@app.route('/articles', methods=['POST'])
def create_article():
    parser = reqparse.RequestParser()

    parser.add_argument('title', help='title cannot be blank', required=True)
    parser.add_argument('text', help='text cannot be blank', required=True)
    parser.add_argument('user_id', help='userId cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.NEW)

    data = parser.parse_args()
    title = data['title']
    text = data['text']
    user_id = int(data['user_id'])
    state = State(data['state'])

    article = Article(
        title=title,
        text=text,
        userId=user_id,
        state=state
    )

    user = User.get_by_id(user_id)

    try:
        article.save_to_db()
        user.articles.append(article)

        return {'message': 'Article was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/articles/<article_id>', methods=['GET'])
def get_article_by_id(article_id: int):
    article = Article.get_by_id(article_id)
    if not article:
        return handle_error_format('Article with such id does not exists.',
                                   'Field \'article_id\' in the request body.'), 404

    return article.to_json()


@app.route('/articles', methods=['GET'])
def get_articles():
    return Article.get_all()


@app.route("/articles/<article_id>", methods=['PUT'])
def update_article(article_id: int):

    parser = reqparse.RequestParser()

    parser.add_argument('title', help='title cannot be blank', required=True)
    parser.add_argument('text', help='text cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.NEW, required=True)

    article = Article.get_by_id(article_id=article_id)

    if article:
        data = parser.parse_args()
        article.title = data['title']
        article.text = data['text']
        article.state = State(data['state'])

        Article.save_to_db(article)

        return Article.to_json(article), 200
    else:
        return {'error': f'Article with id={article_id} does not exist!'}, 404


@app.route('/articles/<article_id>', methods=['DELETE'])
def delete_article(article_id: int):

    try:
        Article.delete_by_id(article_id)
        return {'message': 'Article were deleted'}
    except:
        return {'message': 'Something went wrong'}, 500
