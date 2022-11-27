from unittest import TestCase, mock

from src.model.user import User


class TestUser(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            firstName='first_name',
            lastName='last_name',
            email='email',
            password='password'
        )

    def test_to_json(self):
        user = self.user

        expected_json = {
                         'email': 'email',
                         'firstName': 'first_name',
                         'id': None,
                         'lastName': 'last_name',
                         'roles': [],
                         'username': 'username'}

        result = user.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        user = self.user

        mock_add.return_value = None
        mock_commit.return_value = None

        User.save_to_db(user)

        mock_add.assert_called_once_with(user)
        mock_commit.assert_called_once_with()

    def test_generate_hash(self):
        user = self.user

        result = user.generate_hash('password')

        self.assertTrue(result)

    def test_verify_hash(self):
        user = self.user
        user.password = user.generate_hash('password')

        result = user.verify_hash('password', user.password)

        self.assertTrue(result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_username(self, mock_query_property_getter):
        user = self.user
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = user

        result = User.get_by_username('username')

        self.assertEqual(user, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        user = self.user
        user.id = 1
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = user

        result = User.get_by_id(1)

        self.assertEqual(user, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_username_or_id(self, mock_query_property_getter):
        mock_query_property_getter.return_value.filter.return_value.first.return_value = self.user

        result = User.get_by_username_or_id('username')

        self.assertEqual(self.user, result)

        result = User.get_by_username_or_id(1)

        self.assertEqual(self.user, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def get_by_username_or_id(self, mock_query_property_getter):
        mock_query_property_getter.return_value.filter.return_value.first.return_value = self.user

        result = User.get_by_username_or_email('username')

        self.assertEqual(self.user, result)

        result = User.get_by_username_or_email('email')

        self.assertEqual(self.user, result)

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_email(self, mock_query_property_getter):
        mock_query_property_getter.return_value.filter.return_value.first.return_value = self.user

        result = User.get_by_username_or_id('username')

        self.assertEqual(self.user, result)

        result = User.get_by_username_or_id('email')

        self.assertEqual(self.user, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.user.User.get_by_username_or_id')
    def test_delete_by_identifier(self, mock_get_by_username_or_id, mock_query_property_getter, mock_commit):
        mock_get_by_username_or_id.return_value = self.user
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = User.delete_by_identifier('username')

        self.assertTrue(result)

    @mock.patch('src.model.user.User.get_by_username_or_id')
    def test_delete_by_identifier_with_invalid_user(self, mock_get_by_username_or_id):
        mock_get_by_username_or_id.return_value = None

        result = User.delete_by_identifier('username')

        self.assertEqual(({'errors': [{'message': 'User with such id/username does not exist.',
                                       'source': "Field 'userId/username' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.user.User.get_by_username_or_id')
    def test_delete_by_identifier(self, mock_get_by_username_or_id, mock_query_property_getter, mock_commit):
        mock_get_by_username_or_id.return_value = self.user
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = User.delete_by_identifier('username')

        self.assertTrue(result)
