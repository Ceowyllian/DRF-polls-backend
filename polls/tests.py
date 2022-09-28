import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import (
    APITestCase,
)

from polls import seeder


class TestQuestions(APITestCase):

    @classmethod
    def setUpTestData(cls):
        seeder.run(supress_warnings=True)
        test_user = get_user_model().objects.create_user(
            'test',
            'test@example.com',
            password='test'
        )
        test_token = Token.objects.create(user=test_user)
        cls.test_user = test_user
        cls.test_token = test_token

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_token.key}')

    def test_questions_list(self):
        self.client.logout()
        response = self.client.get(reverse('questions-list'))
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            'Expected Response Code 200, received {0} instead.'
            .format(response.status_code))

    def test_create_question(self):
        question = {
            'question_title': 'test_question',
            'question_text': 'test_text',
            'choices': []
        }
        response = self.client.post(
            path=reverse('questions-list'),
            content_type='application/json',
            data=json.dumps(question))
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            'Expected Response Code 201, received {0} instead.'
            .format(response.status_code))
