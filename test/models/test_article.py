from unittest import TestCase, mock

from src.model.article import Article


class TestUser(TestCase):

    def setUp(self) -> None:
        self.article = Article(
            title='title',
            text='text',
            date='last_name',
            userId='1',
            state='New'
        )

    def test_to_json(self):
        article = self.article

        expected_json = {
            "title": "title",
            'text': "text",
            'date': "last_name",
            'userId': "1",
            'state': "New"}

        result = article.to_json()

        self.assertEqual(expected_json, result)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('src.app.db.session.add')
    def test_save_to_db(self, mock_add, mock_commit):
        article = self.article

        mock_add.return_value = None
        mock_commit.return_value = None

        Article.save_to_db(article)

        mock_add.assert_called_once_with(article)
        mock_commit.assert_called_once_with()

    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    def test_get_by_id(self, mock_query_property_getter):
        article = self.article
        article.id = 1
        mock_query_property_getter.return_value.filter_by.return_value.first.return_value = article

        result = Article.get_by_id(1)

        self.assertEqual(article, result)

    @mock.patch('src.model.article.Article.get_by_id')
    def test_delete_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = Article.delete_by_id(1)

        self.assertEqual(({'errors': [{'message': 'Article with such id does not exist.',
                                       'source': "Field 'articleId' in path parameters."}],
                           'traceId': result[0].get('traceId')}, 404), result)
        mock_get_by_id.assert_called_once_with(1)

    @mock.patch('src.app.db.session.commit')
    @mock.patch('flask_sqlalchemy.model._QueryProperty.__get__')
    @mock.patch('src.model.article.Article.get_by_id')
    def test_delete_by_id(self, mock_get_by_id, mock_query_property_getter, mock_commit):
        article = Article(id=1, title='safa', text='safa', date='fsfs', userId=1, state='New')
        mock_get_by_id.return_value = article
        mock_query_property_getter.return_value.filter_by.return_value.delete.return_value = None
        mock_commit.return_value = None

        result = Article.delete_by_id(1)

        self.assertEqual(article.to_json(), result)
        mock_get_by_id.assert_called_once_with(1)
        mock_query_property_getter.return_value.filter_by.assert_called_once_with(id=1)
        mock_query_property_getter.return_value.filter_by.return_value.delete.assert_called_once_with()
        mock_commit.assert_called_once_with()