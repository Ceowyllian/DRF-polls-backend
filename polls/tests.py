import warnings
from django.http import HttpResponse
from django.test import TestCase
from .seeder import run


class TestQuestionModel(TestCase):

    def setUp(self):
        warnings.simplefilter('ignore')
        run()

    def test_questions(self):
        response: HttpResponse = self.client.get('/polls/questions/')
        self.assertEqual(response.status_code, 200)
