from src.main import app
from src.model.user import User
from src.model.article import State, Article
from flask_restful import reqparse


@app.route('/articles', methods=['POST'])
def create_article():
    parser = reqparse.RequestParser()

    parser.add_argument('title', help='title cannot be blank', required=True)
    parser.add_argument('text', help='text cannot be blank', required=True)
    parser.add_argument('userId', help='userId cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.NEW)

    data = parser.parse_args()
    title = data['title']
    text = data['text']
    user_id = int(data['userId'])
    state = State(data['state'])

    article = Article(
        title=title,
        text=text,
        userId=user_id,
        state=state
    )

    user = User.find_by_id(user_id)

    try:
        article.save_to_db()
        user.articles.append(article)

        return {'message': 'Article was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500
