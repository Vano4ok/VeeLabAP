from unittest import TestCase, mock

from src.model.role import Role


class TestRole(TestCase):

    def test_to_json(self):
        role = Role(id=1, name='user')
        expected_json = {'id': 1, 'name': 'user'}

        result = role.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        role = Role(id=1, name='user')

        mock_add.return_value = None
        mock_commit.return_value = None

        Role.save_to_db(role)

        mock_add.assert_called_once_with(role)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_name(self, mock_query_property_getter):
        role = Role(id=1, name='user')
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = role

        result = Role.get_by_name('user')

        self.assertEqual(role, result)
