import json

from django.contrib.auth import get_user_model
from rest_framework import status

from polls.models import Choice, Vote
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
        cls.uri = "/polls/questions/"
        user, token = cls.create_user_with_token(
            "malihaae6x", "hindy_mauricec1@equipped.twv"
        )
        questions = [Question(**fixtures.question(), created_by=user) for _ in range(5)]
        Question.objects.bulk_create(questions)

    def test_200_questions_exist(self):
        self.client.credentials()
        response = self.client.get(path=self.uri)

        self.assert_status_codes_equal(response.status_code, status.HTTP_200_OK)


class TestQuestionCreate(BaseAPITestCase):
    """
    POST /polls/questions/

    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        cls.uri = "/polls/questions/"
        cls.user, cls.token = cls.create_user_with_token(
            username="keyandran", email="delmer_southwickao@stakeholders.bnh"
        )

    def test_201_created_successfully(self):
        question = fixtures.question_with_choices()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            path=self.uri, content_type="application/json", data=json.dumps(question)
        )

        self.assert_status_codes_equal(response.status_code, status.HTTP_201_CREATED)

    def test_400_cannot_create_invalid_question(self):
        question = fixtures.question_with_choices(
            title=Q.title.too_short(),
            text=Q.text.too_long(),
            choices=fixtures.choice_list(
                number=C.number.too_many(), text=C.text.too_long()
            ),
        )

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(
            path=self.uri, content_type="application/json", data=json.dumps(question)
        )

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_401_cannot_create_unauthorized(self):
        question = fixtures.question_with_choices()

        self.client.credentials()
        response = self.client.post(
            path=self.uri, content_type="application/json", data=json.dumps(question)
        )
        self.assert_status_codes_equal(
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
            username="emelinajyc", email="iraida_descoteauxtwt9@furnishings.if"
        )
        question = Question.objects.create(**fixtures.question(), created_by=user)
        cls.uri = f"/polls/questions/{question.pk}/"

    def test_200_question_exists(self):
        self.client.credentials()
        response = self.client.get(path=self.uri)

        self.assert_status_codes_equal(response.status_code, status.HTTP_200_OK)

    def test_404_non_existent_question(self):
        self.client.credentials()
        response = self.client.get(path="/polls/questions/0/")

        self.assert_status_codes_equal(response.status_code, status.HTTP_404_NOT_FOUND)


class TestQuestionUpdate(BaseAPITestCase):
    """
    PATCH /polls/questions/{id}

    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, token = cls.create_user_with_token(
            username="amanadaj", email="odessa_kaczmarekp2e1@arising.gh"
        )
        cls.user, cls.token = user, token
        question = Question.objects.create(**fixtures.question(), created_by=user)
        cls.question = question
        cls.uri = f"/polls/questions/{question.pk}/"

    def test_200_updated_successfully(self):
        updated_fields = fixtures.question()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(
            path=self.uri,
            content_type="application/json",
            data=json.dumps(updated_fields),
        )

        self.assert_status_codes_equal(response.status_code, status.HTTP_200_OK)

    def test_400_invalid_question_fields(self):
        updated_fields = fixtures.question(
            title=Q.title.too_long(), text=Q.text.too_short()
        )

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(
            path=self.uri,
            content_type="application/json",
            data=json.dumps(updated_fields),
        )

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_401_cannot_update_unauthorized(self):
        updated_fields = fixtures.question()

        self.client.credentials()
        response = self.client.patch(
            path=self.uri,
            content_type="application/json",
            data=json.dumps(updated_fields),
        )

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_403_cannot_update_someone_elses_question(self):
        another_user, another_token = self.create_user_with_token(
            username="shameriat5uz",
            email="pheng_spanndicc@curve.rln",
        )
        updated_fields = fixtures.question()

        self.client.credentials(HTTP_AUTHORIZATION=another_token)
        response = self.client.patch(
            path=self.uri,
            content_type="application/json",
            data=json.dumps(updated_fields),
        )

        self.assert_status_codes_equal(response.status_code, status.HTTP_403_FORBIDDEN)


class TestQuestionDelete(BaseAPITestCase):
    """
    DELETE /polls/question/{id}

    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, token = cls.create_user_with_token(
            username="salamki", email="corie_salamonerci1@translations.nik"
        )
        cls.user, cls.token = user, token
        question = Question.objects.create(**fixtures.question(), created_by=user)
        cls.question = question
        cls.uri = f"/polls/questions/{question.pk}/"

    def test_204_deleted_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response_delete = self.client.delete(self.uri)
        response_retrieve = self.client.get(self.uri)

        self.assert_status_codes_equal(
            response_delete.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assert_status_codes_equal(
            response_retrieve.status_code, status.HTTP_404_NOT_FOUND
        )

    def test_401_cannot_delete_unauthorized(self):
        self.client.credentials()
        response = self.client.delete(self.uri)

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_403_cannot_delete_someone_elses_question(self):
        another_user, another_token = self.create_user_with_token(
            username="loreleipzv", email="filip_hoglunddn@signals.ap"
        )

        self.client.credentials(HTTP_AUTHORIZATION=another_token)
        response = self.client.delete(self.uri)

        self.assert_status_codes_equal(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_404_cannot_delete_non_existent_question(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete("/polls/questions/0/")

        self.assert_status_codes_equal(response.status_code, status.HTTP_404_NOT_FOUND)


class TestVoteCreate(BaseAPITestCase):
    """
    POST /polls/votes/{id}

    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, cls.token = cls.create_user_with_token(
            username="krystatk", email="adams_strumsbs@spare.ll"
        )
        question = Question.objects.create(**fixtures.question(), created_by=user)
        choice_1 = Choice.objects.create(text="Choice 1", question=question)
        choice_2 = Choice.objects.create(text="Choice 2", question=question)
        cls.uri_choice_1 = "/polls/votes/%s/" % choice_1.pk
        cls.uri_choice_2 = "/polls/votes/%s/" % choice_2.pk

    def test_201_vote_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=self.uri_choice_1)

        self.assert_status_codes_equal(response.status_code, status.HTTP_201_CREATED)

    def test_401_cannot_vote_unauthorized(self):
        self.client.credentials()
        response = self.client.post(path=self.uri_choice_1)

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_400_cannot_vote_twice_for_the_same_choice(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response_vote_first = self.client.post(path=self.uri_choice_1)
        response_vote_again = self.client.post(path=self.uri_choice_1)

        self.assert_status_codes_equal(
            response_vote_first.status_code, status.HTTP_201_CREATED
        )
        self.assert_status_codes_equal(
            response_vote_again.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_400_cannot_vote_twice_for_the_same_question(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response_vote_first = self.client.post(path=self.uri_choice_1)
        response_vote_again = self.client.post(path=self.uri_choice_2)

        self.assert_status_codes_equal(
            response_vote_first.status_code, status.HTTP_201_CREATED
        )
        self.assert_status_codes_equal(
            response_vote_again.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_404_cannot_vote_choice_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path="/polls/votes/0/")

        self.assert_status_codes_equal(response.status_code, status.HTTP_404_NOT_FOUND)


class TestVoteDelete(BaseAPITestCase):
    """
    DELETE /polls/votes/{id}

    HTTP authorization IS required.
    """

    @classmethod
    def setUpTestData(cls):
        user, cls.token = cls.create_user_with_token(
            username="krystatk", email="adams_strumsbs@spare.ll"
        )
        question = Question.objects.create(**fixtures.question(), created_by=user)
        choice = Choice.objects.create(text="Choice 1", question=question)
        cls.vote = Vote.objects.create(voted_by=user, choice=choice, question=question)
        cls.uri = f"/polls/votes/{choice.pk}/"

    def test_204_cancel_vote_successfully(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=self.uri)

        self.assert_status_codes_equal(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_401_cannot_cancel_vote_unauthorized(self):
        self.client.credentials()
        response = self.client.delete(path=self.uri)

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_400_cannot_cancel_vote_user_did_not_vote(self):
        self.vote.delete()

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=self.uri)

        self.assert_status_codes_equal(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_404_cannot_cancel_vote_choice_does_not_exist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path="/polls/votes/0/")

        self.assert_status_codes_equal(response.status_code, status.HTTP_404_NOT_FOUND)
