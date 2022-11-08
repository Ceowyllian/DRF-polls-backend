import json

from django.contrib.auth import get_user_model
from rest_framework import status

from polls.models import Choice
from polls.models import Question
from utils.test import BaseAPITestCase
from . import fixtures
from .fixtures import C, Q

User = get_user_model()


class TestQuestionList(BaseAPITestCase):
    """
    GET /polls/questions/
    HTTP authorization is NOT required.
    """

    @classmethod
    def setUpTestData(cls):
        cls.uri = '/polls/questions/'

    def test_200_questions_exist(self):
        self.client.credentials()
        response = self.client.get(path=self.uri)

        self.assert_status_code_equals(
            response.status_code, status.HTTP_200_OK
        )


class TestQuestionCreate(BaseAPITestCase):
    """
    POST /polls/questions/
    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        cls.uri = '/polls/questions/'
        cls.user, cls.token = cls.create_user_with_token(
            username='keyandran',
            email='delmer_southwickao@stakeholders.bnh'
        )

    def test_201_created_successfully(self):
        question = fixtures.question_with_choices()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(question)
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_400_cannot_create_invalid_question(self):
        question = fixtures.question_with_choices(
            title=Q.title.too_short(),
            text=Q.text.too_long(),
            choices=fixtures.choice_list(
                number=C.number.too_many(),
                text=C.text.too_long()
            )
        )

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(question)
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_401_cannot_create_unauthorized(self):
        question = fixtures.question_with_choices()

        self.client.credentials()
        response = self.client.post(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(question)
        )
        self.assert_status_code_equals(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )


class TestQuestionRetrieve(BaseAPITestCase):
    """
    GET /polls/questions/{id}
    HTTP authorization is NOT required.
    """

    @classmethod
    def setUpTestData(cls):
        user, token = cls.create_user_with_token(
            username='emelinajyc',
            email='iraida_descoteauxtwt9@furnishings.if'
        )
        question = Question.objects.create(
            **fixtures.question(),
            created_by=user
        )
        cls.uri = f'/polls/questions/{question.pk}/'

    def test_200_question_exists(self):
        self.client.credentials()
        response = self.client.get(path=self.uri)

        self.assert_status_code_equals(
            response.status_code, status.HTTP_200_OK
        )

    def test_404_non_existent_question(self):
        self.client.credentials()
        response = self.client.get(path='/polls/questions/0/')

        self.assert_status_code_equals(
            response.status_code, status.HTTP_404_NOT_FOUND
        )


class TestQuestionUpdate(BaseAPITestCase):
    """
    PATCH /polls/questions/{id}
    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, token = cls.create_user_with_token(
            username='amanadaj',
            email='odessa_kaczmarekp2e1@arising.gh'
        )
        cls.user, cls.token = user, token
        question = Question.objects.create(
            **fixtures.question(),
            created_by=user
        )
        cls.question = question
        cls.uri = f'/polls/questions/{question.pk}/'

    def test_200_updated_successfully(self):
        updated_fields = fixtures.question()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(updated_fields)
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_200_OK
        )

    def test_400_invalid_question_fields(self):
        updated_fields = fixtures.question(
            title=Q.title.too_long(),
            text=Q.text.too_short()
        )

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(updated_fields)
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_401_cannot_update_unauthorized(self):
        updated_fields = fixtures.question()

        self.client.credentials()
        response = self.client.patch(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(updated_fields)
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_403_cannot_update_someone_elses_question(self):
        another_user, another_token = self.create_user_with_token(
            username='shameriat5uz',
            email='pheng_spanndicc@curve.rln',
        )
        updated_fields = fixtures.question()

        self.client.credentials(HTTP_AUTHORIZATION=another_token)
        response = self.client.patch(
            path=self.uri,
            content_type='application/json',
            data=json.dumps(updated_fields)
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_403_FORBIDDEN
        )


class TestQuestionDelete(BaseAPITestCase):
    """
    DELETE /polls/question/{id}
    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, token = cls.create_user_with_token(
            username='salamki',
            email='corie_salamonerci1@translations.nik'
        )
        cls.user, cls.token = user, token
        question = Question.objects.create(
            **fixtures.question(),
            created_by=user
        )
        cls.question = question
        cls.uri = f'/polls/questions/{question.pk}/'

    def test_204_deleted_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response_delete = self.client.delete(self.uri)
        response_retrieve = self.client.get(self.uri)

        self.assert_status_code_equals(
            response_delete.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assert_status_code_equals(
            response_retrieve.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_401_cannot_delete_unauthorized(self):
        self.client.credentials()
        response = self.client.delete(self.uri)

        self.assert_status_code_equals(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_403_cannot_delete_someone_elses_question(self):
        another_user, another_token = self.create_user_with_token(
            username='loreleipzv',
            email='filip_hoglunddn@signals.ap'
        )

        self.client.credentials(HTTP_AUTHORIZATION=another_token)
        response = self.client.delete(self.uri)

        self.assert_status_code_equals(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_404_cannot_delete_non_existent_question(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete('/polls/questions/0/')

        self.assert_status_code_equals(
            response.status_code, status.HTTP_404_NOT_FOUND
        )


class TestVoteCreate(BaseAPITestCase):
    """
    POST /polls/votes/
    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, token = cls.create_user_with_token(
            username='krystatk',
            email='adams_strumsbs@spare.ll'
        )
        question = Question.objects.create(
            **fixtures.question(),
            created_by=user
        )
        choice_1 = Choice.objects.create(
            choice_text='Choice 1',
            question=question
        )
        choice_2 = Choice.objects.create(
            choice_text='Choice 2',
            question=question
        )
        cls.token = token
        cls.choice_1 = choice_1
        cls.choice_2 = choice_2
        cls.uri = '/polls/votes/'

    def test_201_vote_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            path=self.uri,
            content_type='application/json',
            data=json.dumps({'choice_pk': self.choice_1.pk})
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_401_cannot_vote_unauthorized(self):
        self.client.credentials()
        response = self.client.post(
            path=self.uri,
            content_type='application/json',
            data=json.dumps({'choice_pk': self.choice_1.pk})
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_400_cannot_vote_twice_for_the_same_choice(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        kwargs = {
            'path': self.uri,
            'content_type': 'application/json',
            'data': json.dumps({'choice_pk': self.choice_1.pk})
        }
        response_vote_1 = self.client.post(**kwargs)
        response_vote_2 = self.client.post(**kwargs)

        self.assert_status_code_equals(
            response_vote_1.status_code,
            status.HTTP_201_CREATED
        )
        self.assert_status_code_equals(
            response_vote_2.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_400_cannot_vote_twice_for_the_same_question(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        kwargs = {
            'path': self.uri,
            'content_type': 'application/json',
        }
        response_vote_1 = self.client.post(
            **kwargs,
            data=json.dumps({'choice_pk': self.choice_1.pk})
        )
        response_vote_2 = self.client.post(
            **kwargs,
            data=json.dumps({'choice_pk': self.choice_2.pk})
        )

        self.assert_status_code_equals(
            response_vote_1.status_code,
            status.HTTP_201_CREATED
        )
        self.assert_status_code_equals(
            response_vote_2.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_400_cannot_vote_choice_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        response = self.client.post(
            path=self.uri,
            content_type='application/json',
            data=json.dumps({'choice_pk': 'blablabla'})
        )

        self.assert_status_code_equals(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
