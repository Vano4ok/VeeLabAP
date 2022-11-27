from unittest import TestCase, mock
from undecorated import undecorated
from src.model.user import User
from src.model.role import Role
from src.model.article import Article

from src.route import create_article, get_article_by_id, delete_article


class TestAccounts(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            firstName='first_name',
            lastName='last_name',
            email='email',
            password='password'
        )

        self.article = Article(
            title='titlefcc',
            text='text',
            userId=1,
            state='New'
        )

        self.article_json_create = {
            'title': 'title',
            'text': 'text',
            'user_id': 1,
            'state': 'New'
        }

        self.user_role = Role(
            id=1,
            name='user'
        )

        self.admin_role = Role(
            id=2,
            name='admin'
        )

        self.user.articles.append(self.article)
        self.user.roles.append(self.user_role)

    @mock.patch('src.model.article.Article.save_to_db')
    @mock.patch('src.model.user.User.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_article(self, mock_request_parser, mock_get_by_id, mock_save_to_db):
        mock_request_parser.return_value = self.article_json_create
        mock_get_by_id.return_value = self.user
        mock_save_to_db.return_value = True

        result = create_article()

        self.assertEqual(({'message': 'Article was successfully created'}, 200), result)

    @mock.patch('src.model.article.Article.save_to_db')
    @mock.patch('src.model.user.User.get_by_id')
    @mock.patch('flask_restful.reqparse.RequestParser.parse_args')
    def test_create_article_with_invalid_user(self, mock_request_parser, mock_get_by_id, mock_save_to_db):
        mock_request_parser.return_value = self.article_json_create
        mock_get_by_id.return_value = None
        mock_save_to_db.return_value = True

        result = create_article()

        self.assertEqual(({'message': 'Something went wrong'}, 500), result)

    @mock.patch('src.model.Article.delete_by_id')
    @mock.patch('src.model.Article.get_by_id')
    @mock.patch('src.model.Role.get_by_name')
    @mock.patch('src.model.User.get_by_username')
    @mock.patch('flask_httpauth.HTTPAuth.current_user')
    def test_delete_article_by_id(self, mock_current_user, mock_get_by_username, mock_get_by_name, mock_get_by_id,
                                  mock_delete_by_id):
        mock_current_user.return_value = 'username'
        mock_get_by_username.return_value = self.user
        mock_get_by_name.return_value = self.admin_role
        mock_get_by_id.return_value = self.article
        mock_delete_by_id.return_value = self.article.to_json()

        undecorated_delete_account_by_id = undecorated(delete_article)
        result = undecorated_delete_account_by_id(1)

        self.assertEqual({'message': 'Article were deleted'}, result)

    @mock.patch('src.model.Article.save_to_db')
    @mock.patch('src.model.Article.get_by_id')
    def test_get_article_by_id(self, mock_get_by_id, mock_save_to_db):
        mock_get_by_id.return_value = self.article
        mock_save_to_db.return_value = True

        undecorated_get_account_by_id = undecorated(get_article_by_id)
        result = undecorated_get_account_by_id(1)

        self.assertEqual({'date': None, 'state': 'New', 'text': 'text', 'title': 'titlefcc', 'userId': 1}, result)

    @mock.patch('src.model.Article.get_by_id')
    def test_get_article_by_id_with_invalid_account_id(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        undecorated_get_article_by_id = undecorated(get_article_by_id)
        result = undecorated_get_article_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Article with such id does not exists.',
                                       'source': "Field 'article_id' in the request body."}],
                           'traceId': result[0].get('traceId')}, 404), result)
