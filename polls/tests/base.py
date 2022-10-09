from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from polls import seeder
from polls.models import Question, Choice


class PollsAPITestCase(APITestCase):
    """
    The base class for polls API tests, which sets up test data and automatic
    client authorization before each test.
    """

    @classmethod
    def setUpTestData(cls):
        seeder.run(supress_warnings=True)
        test_user = get_user_model().objects.create_user(
            'test',
            'test@example.com',
            password='test')
        test_token = Token.objects.create(user=test_user)
        cls.test_user = test_user
        cls.test_token = test_token

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_token.key}')

    def _test_question(self):
        kwargs = {
            'question_title': 'Test question title',
            'question_text': 'Test question text',
            'created_by': self.test_user,
        }

        question, created = Question.objects.get_or_create(**kwargs)
        if created:
            question.delete()
            question = Question.objects.create(**kwargs)

        return question

    def assertStatusCodeEquals(self, received, expected):
        self.assertEqual(
            received, expected,
            'Expected Response Code {0}, received {1} instead.'
            .format(expected, received))
