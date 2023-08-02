import pytest
from django.core.exceptions import PermissionDenied, ValidationError

from api.common import pagination
from api.polls import views
from apps.polls.models import Choice, Question


class TestQuestionList:
    """
    GET /polls/questions/

    HTTP authorization is NOT required.
    """

    uri = "/api/polls/questions/"

    def test_200_questions_exist(self, monkeypatch, api_client):
        def paginate_queryset_mock(paginator_instance, *args, **kwargs):
            paginator_instance.has_next = False
            paginator_instance.has_previous = False
            return Question.objects.none()

        monkeypatch.setattr(views.QuestionViewSet, "queryset", Question.objects.none())
        monkeypatch.setattr(
            pagination.CursorPagination, "paginate_queryset", paginate_queryset_mock
        )

        response = api_client.get(self.uri)

        assert response.status_code == 200


class TestQuestionCreate:
    """
    POST /polls/questions/

    HTTP authorization IS required.
    """

    uri = "/api/polls/questions/"

    def test_201_created_successfully(
        self, monkeypatch, api_client, user, valid_question_dict
    ):
        def create_mock(**kwargs):
            question = Question(title="blablabla", text="blablabla", created_by=user)
            question.pk = 0
            return question

        monkeypatch.setattr(views, "question_create", create_mock)

        api_client.force_authenticate(user)
        response = api_client.post(self.uri, data=valid_question_dict)

        assert response.status_code == 201

    def test_400_cannot_create_invalid_question(
        self, monkeypatch, api_client, user, invalid_question_dict
    ):
        def create_mock(*args, **kwargs):
            raise ValidationError("")

        monkeypatch.setattr(views, "question_create", create_mock)

        api_client.force_authenticate(user)
        response = api_client.post(self.uri, data=invalid_question_dict)

        assert response.status_code == 400

    def test_401_cannot_create_unauthorized(self, api_client, valid_question_dict):
        response = api_client.post(self.uri, data=valid_question_dict)

        assert response.status_code == 401


class TestQuestionRetrieve:
    """
    GET /polls/questions/{id}/

    HTTP authorization is NOT required.
    """

    uri = "/api/polls/questions/123/"

    def test_200_question_exists(self, monkeypatch, api_client, question):
        def retrieve_mock(*args, **kwargs):
            return question

        monkeypatch.setattr(views.QuestionViewSet, "get_object", retrieve_mock)
        response = api_client.get(self.uri)

        assert response.status_code == 200

    def test_404_non_existent_question(self, monkeypatch, api_client):
        def retrieve_mock(*args, **kwargs):
            raise Question.DoesNotExist

        monkeypatch.setattr(views.QuestionViewSet, "get_object", retrieve_mock)

        response = api_client.get(self.uri)

        assert response.status_code == 404


class TestQuestionUpdate:
    """
    PATCH /polls/questions/{id}/

    HTTP authorization IS required.
    """

    uri = "/api/polls/questions/123/"

    @pytest.fixture(scope="class")
    def updated_fields(self):
        return {
            "title": "9a036a82-9833-abcd-4dda-b8e1-01f894b598f7",
            "text": "uUhe0kGrG0cAMVMHl7NSErKlPSWHsRV5LfPDUxyRlXmgazsPf93YWj",
        }

    def test_200_updated_successfully(
        self, monkeypatch, api_client, user, question, updated_fields
    ):
        def update_mock(*args, **kwargs):
            question.title = updated_fields["title"]
            question.text = updated_fields["text"]
            return question

        monkeypatch.setattr(views, "question_update", update_mock)
        api_client.force_authenticate(user)
        response = api_client.patch(self.uri, data=updated_fields)

        assert response.status_code == 200

    def test_400_invalid_question_fields(self, monkeypatch, api_client, user):
        def update_mock(*args, **kwargs):
            raise ValidationError("")

        monkeypatch.setattr(views, "question_update", update_mock)
        api_client.force_authenticate(user)
        response = api_client.patch(self.uri, data={"title": "", "text": None})

        assert response.status_code == 400

    def test_401_cannot_update_unauthorized(
        self, monkeypatch, api_client, updated_fields
    ):
        def should_not_be_called(*args, **kwargs):
            raise AssertionError("Question update service shouldn't be called!")

        monkeypatch.setattr(views, "question_update", should_not_be_called)
        response = api_client.patch(self.uri, data=updated_fields)
        assert response.status_code == 401

    def test_403_cannot_update_someone_elses_question(
        self, monkeypatch, api_client, user, updated_fields
    ):
        def update_mock(*args, **kwargs):
            raise PermissionDenied("Nope, lol")

        monkeypatch.setattr(views, "question_update", update_mock)
        api_client.force_authenticate(user)
        response = api_client.patch(self.uri, data=updated_fields)

        assert response.status_code == 403


class TestQuestionDelete:
    """
    DELETE /polls/question/{id}/

    HTTP authorization IS required.
    """

    uri = "/api/polls/questions/123/"

    def test_204_deleted_successfully(self, monkeypatch, api_client, user):
        def destroy_mock(*args, **kwargs):
            pass

        monkeypatch.setattr(views, "question_destroy", destroy_mock)

        api_client.force_authenticate(user)
        response = api_client.delete(self.uri)

        assert response.status_code == 204

    def test_401_cannot_delete_unauthorized(self, monkeypatch, api_client):
        def should_not_be_called(*args, **kwargs):
            raise AssertionError("Question update service shouldn't be called!")

        monkeypatch.setattr(views, "question_destroy", should_not_be_called)

        response = api_client.delete(self.uri)
        assert response.status_code == 401

    def test_403_cannot_delete_someone_elses_question(
        self, monkeypatch, api_client, user
    ):
        def destroy_mock(*args, **kwargs):
            raise PermissionDenied("Nope, lol")

        monkeypatch.setattr(views, "question_destroy", destroy_mock)

        api_client.force_authenticate(user)
        response = api_client.delete(self.uri)
        assert response.status_code == 403

    def test_404_cannot_delete_non_existent_question(
        self, monkeypatch, api_client, user
    ):
        def destroy_mock(*args, **kwargs):
            raise Question.DoesNotExist

        monkeypatch.setattr(views, "question_destroy", destroy_mock)

        api_client.force_authenticate(user)
        response = api_client.delete(self.uri)

        assert response.status_code == 404


class TestVoteCreate:
    """
    POST /polls/votes/{id}/

    HTTP authorization IS required.
    """

    uri = "/api/polls/votes/123/"

    def test_201_vote_successfully(self, monkeypatch, api_client, user):
        def perform_vote_mock(*args, **kwargs):
            pass

        monkeypatch.setattr(views, "perform_vote", perform_vote_mock)

        api_client.force_authenticate(user)
        response = api_client.post(self.uri)

        assert response.status_code == 201

    def test_401_cannot_vote_unauthorized(self, monkeypatch, api_client):
        def should_not_be_called(*args, **kwargs):
            raise AssertionError("Vote perform service shouldn't be called!")

        monkeypatch.setattr(views, "perform_vote", should_not_be_called)

        response = api_client.post(self.uri)

        assert response.status_code == 401

    def test_400_cannot_vote_twice_for_the_same_choice(
        self, monkeypatch, api_client, user
    ):
        class PerformVoteMock:
            def __init__(self):
                self.number_of_calls = 0

            def __call__(self, *args, **kwargs):
                self.number_of_calls += 1
                if self.number_of_calls > 1:
                    raise ValidationError("Too many calls, lol")

        monkeypatch.setattr(views, "perform_vote", PerformVoteMock())

        api_client.force_authenticate(user)
        response_vote_first = api_client.post(self.uri)
        response_vote_second = api_client.post(self.uri)

        assert response_vote_first.status_code == 201
        assert response_vote_second.status_code == 400

    def test_404_cannot_vote_choice_does_not_exist(self, monkeypatch, api_client, user):
        def perform_vote_mock(*args, **kwargs):
            raise Choice.DoesNotExist

        monkeypatch.setattr(views, "perform_vote", perform_vote_mock)

        api_client.force_authenticate(user)
        response = api_client.post(self.uri)

        assert response.status_code == 404


class TestVoteDelete:
    """
    DELETE /polls/votes/{id}/

    HTTP authorization IS required.
    """

    uri = "/api/polls/votes/123/"

    def test_204_cancel_vote_successfully(self, monkeypatch, api_client, user):
        def cancel_vote_mock(*args, **kwargs):
            pass

        monkeypatch.setattr(views, "cancel_vote", cancel_vote_mock)

        api_client.force_authenticate(user)
        response = api_client.delete(self.uri)

        assert response.status_code == 204

    def test_401_cannot_cancel_vote_unauthorized(self, monkeypatch, api_client, user):
        def should_not_be_called(*args, **kwargs):
            raise AssertionError("Cancel vote service should not be called!")

        monkeypatch.setattr(views, "cancel_vote", should_not_be_called)

        response = api_client.delete(self.uri)

        assert response.status_code == 401

    def test_400_cannot_cancel_vote_user_did_not_vote(
        self, monkeypatch, api_client, user
    ):
        def cancel_vote_mock(*args, **kwargs):
            raise ValidationError("")

        monkeypatch.setattr(views, "cancel_vote", cancel_vote_mock)

        api_client.force_authenticate(user)
        response = api_client.delete(self.uri)

        assert response.status_code == 400

    def test_404_cannot_cancel_vote_choice_does_not_exist(
        self, monkeypatch, api_client, user
    ):
        def cancel_vote_mock(*args, **kwargs):
            raise Choice.DoesNotExist

        monkeypatch.setattr(views, "cancel_vote", cancel_vote_mock)

        api_client.force_authenticate(user)
        response = api_client.delete(self.uri)

        assert response.status_code == 404
