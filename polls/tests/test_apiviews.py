import json

from rest_framework import status
from rest_framework.reverse import reverse

from polls.models import Choice
from .base import PollsAPITestCase


class TestQuestionViewSet(PollsAPITestCase):
    """
    Tests for QuestionViewSet (list, create, retrieve, update, delete).
    """

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


class TestVoteAPI(PollsAPITestCase):

    def test_vote(self):
        choice = Choice.objects.create(
            choice_text='Test choice',
            question=self._test_question()
        )
        url = reverse('vote')

        response = self.client.post(url, data={
            'choice': choice.pk,
        })

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_201_CREATED)

    def test_fail_vote_twice(self):
        choice = Choice.objects.create(
            choice_text='Test choice',
            question=self._test_question()
        )
        url = reverse('vote')

        response_vote_1 = self.client.post(url, data={
            'choice': choice.pk
        })
        response_vote_2 = self.client.post(url, data={
            'choice': choice.pk
        })

        self.assertStatusCodeEquals(
            response_vote_1.status_code, status.HTTP_201_CREATED)
        self.assertStatusCodeEquals(
            response_vote_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_vote_unauthorized(self):
        choice = Choice.objects.create(
            choice_text='Test choice',
            question=self._test_question()
        )
        url = reverse('vote')

        self.client.logout()
        response = self.client.post(url, data={
            'choice': choice.pk
        })

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_choice_does_not_exist(self):
        non_existent_choice = 'bla bla bla'
        url = reverse('vote')

        response = self.client.post(url, data={
            'choice': non_existent_choice
        })

        self.assertStatusCodeEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST)
