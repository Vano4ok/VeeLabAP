from src.model.user import User
from src.model.role import Role
from unittest import TestCase, mock
from undecorated import undecorated
from src.route.auth import verify_password, get_user_roles


class TestAuth(TestCase):

    def setUp(self) -> None:
        self.user = User(
            username='username',
            firstName='first_name',
            lastName='last_name',
            email='email',
            password='password'
        )

        self.user.roles.append(Role(id=1, name='user'))
        self.user.roles.append(Role(id=2, name='admin'))

    @mock.patch('src.model.user.User.verify_hash')
    @mock.patch('src.model.user.User.get_by_username_or_id')
    def test_verify_password(self, mock_get_by_username_or_email, mock_verify_hash):
        mock_get_by_username_or_email.return_value = self.user
        mock_verify_hash.return_value = True

        undecorated_verify_password = undecorated(verify_password)
        result = undecorated_verify_password('username', 'password')

        self.assertEqual('username', result)

    @mock.patch('src.model.user.User.get_by_username')
    def test_get_user_roles(self, mock_get_by_username):
        mock_get_by_username.return_value = self.user

        undecorated_get_user_roles = undecorated(get_user_roles)
        result = undecorated_get_user_roles('username')

        self.assertEqual(['user', 'admin'], result)
