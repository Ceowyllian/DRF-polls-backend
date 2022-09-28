import warnings

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

from polls import apiviews
from . import seeder
from .models import Question


class TestQuestionList(APITestCase):

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            'test@example.com',
            password='test'
        )

    def setUp(self):
        seeder.run(supress_warnings=True)

        self.factory = APIRequestFactory()
        self.view = apiviews.QuestionViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })
        self.uri = '/questions/'

        self.user = self.setup_user()
        token = Token.objects.create(user=self.user)
        token.save()
        self.AUTH = f'Token {token.key}'

    def test_get(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION=self.AUTH
        )
        request.user = self.user
        response = self.view(request)
        self.assertEqual(
            response.status_code, 200,
            'Expected Response Code 200, received {0} instead.'
            .format(response.status_code)
        )

    def test_post(self):
        request = self.factory.post(
            self.uri,
            HTTP_AUTHORIZATION=self.AUTH,
            data={
                'question_title': 'test_question',
                'question_text': 'test_text',
                'choices': []
            }
        )
        response = self.view(request)
        self.assertEqual(
            response.status_code, 201,
            'Expected Response Code 201, received {0} instead.'
            .format(response.status_code)
        )



