import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from polls import seeder
from polls.models import Question


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

    def assertStatusCodeEquals(self, received, expected):
        self.assertEqual(
            received, expected,
            'Expected Response Code {0}, received {1} instead.'
            .format(expected, received))


class TestQuestionViewSet(PollsAPITestCase):
    """
    Tests for QuestionViewSet (list, create, retrieve, update, delete).
    """

    def _test_question(self):
        return Question.objects.get_or_create(
            question_title='Test question title',
            question_text='Test question text.',
            created_by=self.test_user
        )[0]

    def test_list(self):
        """
        Testing the "GET" method for the "/questions" endpoint.
        """

        # The question list should be available without authorization.
        self.client.logout()

        response = self.client.get(reverse('question-list'))

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_200_OK)

    def test_create_with_choices(self):
        """
        Testing the "POST" method for the "/questions" endpoint.
        """

        question = {
            'question_title': 'test_question',
            'question_text': 'test_text',
            'choices': [
                {'choice_text': 'choice 1'},
                {'choice_text': 'choice 2'},
                {'choice_text': 'choice 3'},
            ]
        }

        response = self.client.post(
            path=reverse('question-list'),
            content_type='application/json',
            data=json.dumps(question))

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_with_empty_choices(self):
        """
        Testing the "POST" method for the "/questions" endpoint.
        """

        question = {
            'question_title': 'test_question',
            'question_text': 'test_text',
            'choices': []
        }

        response = self.client.post(
            path=reverse('question-list'),
            content_type='application/json',
            data=json.dumps(question))
        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_with_invalid_choices(self):
        """
        Testing the "POST" method for the "/questions" endpoint.
        """

        question = {
            'question_title': 'test_question',
            'question_text': 'test_text',
            'choices': [
                {'choice_text': ''},
                {'choice_text': ''},
                {'choice_text': ''},
                {'choice_text': ''},
            ]
        }

        response = self.client.post(
            path=reverse('question-list'),
            content_type='application/json',
            data=json.dumps(question))

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_without_choices(self):
        """
        Testing the "POST" method for the "/questions" endpoint.
        """

        question = {
            'question_title': 'test_question',
            'question_text': 'test_text',
        }

        response = self.client.post(
            path=reverse('question-list'),
            content_type='application/json',
            data=json.dumps(question))

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        """
        Testing the "GET" method for the "/questions/<id>" endpoint.
        """

        # The question detail should be available without authorization.
        self.client.logout()

        question = self._test_question()

        response = self.client.get(
            path=reverse('question-detail', args=[question.pk]))

        self.assertStatusCodeEquals(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['question_title'], question.question_title)
        self.assertEqual(data['question_text'], question.question_text)
        self.assertEqual(data['created_by'], self.test_user.pk)

    def test_update(self):
        """
        Testing the "PATCH" method for the "/questions/<id>" endpoint.
        """

        question = self._test_question()
        updated_fields = {
            'question_title': 'Another title',
            'question_text': 'Another text',
        }

        response = self.client.patch(
            path=reverse('question-detail', args=[question.pk]),
            content_type='application/json',
            data=json.dumps(updated_fields))

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        """
        Testing the "DELETE" method for the "/questions/<id>" endpoint.
        """

        question = self._test_question()
        question_id = question.pk

        response_delete = self.client.delete(
            reverse('question-detail', args=[question_id]))
        self.assertStatusCodeEquals(
            response_delete.status_code, status.HTTP_204_NO_CONTENT)

        response_retrieve = self.client.get(
            reverse('question-detail', args=[question_id]))
        self.assertStatusCodeEquals(
            response_retrieve.status_code, status.HTTP_404_NOT_FOUND)
